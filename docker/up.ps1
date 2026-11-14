# Start the stack with this computer's own fonts mounted beside the operator's folder.
#
# Compose cannot detect a platform and has no optional mount: a source it cannot find stops the whole
# stack. So the directories are chosen here, written to a small override, and passed as a second -f.
# Plain `docker compose up` keeps working - it mounts the operator's folder and nothing else.
#
#   docker\up.ps1              # up -d, with this computer's fonts
#   docker\up.ps1 --build      # up -d --build
#   docker\up.ps1 --print      # show the merged configuration, start nothing
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

$override = Join-Path ([System.IO.Path]::GetTempPath()) 'gkps-host-fonts.yaml'
$candidates = @('C:/Windows/Fonts')
if ($env:LOCALAPPDATA) { $candidates += (Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts') }
if ($env:USERPROFILE) { $candidates += (Join-Path $env:USERPROFILE '.local\share\gkps-fonts') }

$lines = @('services:', '  media:', '    volumes:')
$count = 0
$added = @()
$labels = ''
foreach ($dir in $candidates) {
    if (-not (Test-Path -LiteralPath $dir -PathType Container)) { continue }
    $count++
    $quoted = ($dir -replace '\\', '/') -replace "'", "''"
    $added += $quoted
    if ($labels) { $labels += ',' }
    $labels += "$count=$quoted"
    $lines += '      - type: bind'
    $lines += "        source: '$quoted'"
    $lines += "        target: /usr/share/fonts/host/$count"
    $lines += '        read_only: true'
}
if ($count -eq 0) { $lines[-1] = '    volumes: []' }
else {
    $lines += '    environment:'
    $lines += "      GKPS_MEDIA_FONT_LABELS: '$labels'"
}
[System.IO.File]::WriteAllLines($override, $lines)

$printOnly = $false
$rest = @()
if ($args.Count -gt 0 -and $args[0] -eq '--print') {
    $printOnly = $true
    if ($args.Count -gt 1) { $rest = $args[1..($args.Count - 1)] }
}
elseif ($args.Count -gt 0) {
    $rest = $args
}

if ($rest.Count -eq 0 -and -not $printOnly) { $rest = @('up', '-d') }
elseif ($rest.Count -gt 0 -and $rest[0].StartsWith('-')) { $rest = @('up', '-d') + $rest }

if ($count -eq 0) {
    Write-Output 'gkps: no font directory found on this computer'
} else {
    Write-Output "gkps: font directories from this computer ($count):"
    foreach ($dir in $added) { Write-Output "gkps:   $dir" }
}

$composeArgs = @('-f', 'docker-compose.yml', '-f', $override)
if ($printOnly) {
    & docker compose @composeArgs config @rest
    exit $LASTEXITCODE
}

& docker compose @composeArgs @rest
$status = $LASTEXITCODE

# A shared path Docker cannot read mounts as an empty directory without an error, so the start is
# followed by one look inside: nothing visible means the operator is told instead of quietly drawing
# with the image's faces.
if ($status -eq 0 -and $count -gt 0 -and $rest[0] -eq 'up') {
    $seen = (& docker compose @composeArgs exec -T media sh -c 'fc-list 2>/dev/null | grep -c "/usr/share/fonts/host/"') 2>$null
    if (-not $seen -or [int]$seen -eq 0) {
        Write-Output 'gkps: the mounted font directories showed no font to the companion'
        Write-Output 'gkps: check Docker > Settings > Resources > File Sharing for the paths above'
    }
}

exit $status
