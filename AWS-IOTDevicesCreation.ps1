#$devices = @('1','2','3','4','5','6')
$devices = @()
for($i=4; $i -le 50; $i++){ $devices += $i.ToString()}


# Create certificates and attach them to the policy for each device
cd 'C:\Users\'
foreach ($device in $devices)
{
    #Create Certificate
	$deviceName = 'device'+$device
    Write-Host "public_$($deviceName).key"
	$certificate = aws iot create-keys-and-certificate --set-as-active --certificate-pem-outfile "$($deviceName)_certificate.pem" --public-key-outfile "public_$($deviceName).key" --private-key-outfile "private_$($deviceName).key" | ConvertFrom-Json
	aws iot attach-policy  --target $certificate.certificateArn  --policy-name iot-devices-policy
    Write-Host "Thing $($deviceName) created"

	#Create IoT Thing
    Write-Host "Thing $($deviceName) created"
	aws iot create-thing --thing-name $deviceName
	aws iot attach-thing-principal --principal $certificate.certificateArn --thing-name $deviceName
                    
}
