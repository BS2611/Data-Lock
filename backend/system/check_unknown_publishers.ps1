# check_unknown_publishers.ps1

# Function to check if the path is a known system path
function Is-KnownSystemPath {
    param (
        [string]$path
    )
    return $path -match "^(C:\\Program Files\\WindowsApps\\)"
}

# Get all running processes
$processes = Get-Process | Where-Object { $_.Path -and (Test-Path $_.Path) }

$result = @()

foreach ($proc in $processes) {
    if (-not (Is-KnownSystemPath $proc.Path)) {
        $signInfo = Get-AuthenticodeSignature $proc.Path
        $publisher = if ($signInfo.Status -eq 'Valid') { $signInfo.SignerCertificate.Subject } else { "Unknown" }

        if ($publisher -eq "Unknown") {
            $processInfo = @{
                ProcessName = $proc.Name
                ProcessId = $proc.Id
                Path = $proc.Path
                Publisher = $publisher
            }
            $result += $processInfo
        }
    }
}

# Output result as a valid JSON array
$result | ConvertTo-Json -Compress
