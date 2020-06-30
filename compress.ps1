Get-Location
Set-Location $PSScriptRoot
Get-Location

$python =  "python"
$python
IF (Test-Path -Path $python) {
    "Python exist, deleting"
    Remove-Item -Path $python -Recurse
}

New-Item -Name $python -ItemType "directory" -Force

$zip = Join-Path -Path $PSScriptRoot -ChildPath $python
Copy-Item "*.py", "LICENSE", "README.md" -Destination $zip

$compress = @{
  Path = $zip
  CompressionLevel = "Fastest"
  DestinationPath = "CryptoPriceLambdaCommons.zip"
}

Compress-Archive @compress -Force
Remove-Item -Path $python -Recurse