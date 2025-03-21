<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mac_address = escapeshellarg($_POST['mac_address']);
    $dhcp_version = escapeshellarg($_POST['dhcp_version']);

    // Execute Python script
    $command = "python3 network_config.py $mac_address $dhcp_version";
    $output = shell_exec($command);

    // Decode JSON response
    $response = json_decode($output, true);
} else {
    $response = ["error" => "Invalid request method."];
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>DHCP IP Assignment</title>
</head>
<body>
    <h2>DHCP IP Assignment Results:</h2>
    <?php if (isset($response["error"])): ?>
        <p style="color: red;"><?php echo htmlspecialchars($response["error"]); ?></p>
    <?php else: ?>
        <p><strong>MAC Address:</strong> <?php echo htmlspecialchars($response["mac_address"]); ?></p>
        <p><strong>Assigned IP:</strong> <?php echo htmlspecialchars($response["assigned_ip"]); ?></p>
        <p><strong>Lease Duration:</strong> <?php echo htmlspecialchars($response["lease_time"]); ?></p>
    <?php endif; ?>
</body>
</html>
