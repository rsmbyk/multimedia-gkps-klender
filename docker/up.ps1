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
# with the image's faces. The count is asked for through a command that always succeeds, so a non-zero
# status from `exec` can only mean the container — not a grep that matched nothing. PowerShell 5.1
# turns a native command's stderr into a terminating error under 'Stop', which is why the block runs
# under 'Continue': a companion that is not running is reported, never thrown, and the start's own
# status is what the script exits with.
if ($status -eq 0 -and $count -gt 0 -and $rest[0] -eq 'up') {
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $seen = (& docker compose @composeArgs exec -T media sh -c 'n=$(fc-list 2>/dev/null | grep -c "/usr/share/fonts/host/"); printf "%s" "$n"; exit 0' 2>$null)
    $checked = $LASTEXITCODE
    $counted = "$seen".Trim()
    $detail = ''
    if ($checked -ne 0 -or $counted -notmatch '^\d+$') {
        $detail = (& docker compose @composeArgs logs --no-color --tail 1 media 2>$null | Select-Object -Last 1)
    }
    $ErrorActionPreference = $previousPreference
    if ($checked -ne 0 -or $counted -notmatch '^\d+$') {
        # "container is restarting" names nothing; the companion's own line names the cause, and a
        # start that follows a pull without a rebuild is the common one (spec 218).
        Write-Output 'gkps: the media companion is not running — the font mounts were not checked'
        if ($detail) { Write-Output "gkps: its last line: $detail" }
        Write-Output 'gkps: see docker compose logs media; if the image predates your checkout, docker compose build'
    }
    elseif ([int]$counted -eq 0) {
        Write-Output 'gkps: the mounted font directories showed no font to the companion'
        Write-Output 'gkps: check Docker > Settings > Resources > File Sharing for the paths above'
    }
}

exit $status
