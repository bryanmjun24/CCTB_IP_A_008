<!DOCTYPE html>
<html>
<head>
    <title>DHCP IP Request Form</title>
</head>
<body>
    <h2>Request an IP Address</h2>
    <form action="process.php" method="post">
        <label>Enter MAC Address (e.g., 00:1A:2B:3C:4D:5E):</label><br>
        <input type="text" name="mac_address" required pattern="^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"><br><br>

        <label>Select DHCP Version:</label><br>
        <input type="radio" name="dhcp_version" value="DHCPv4" required> DHCPv4<br>
        <input type="radio" name="dhcp_version" value="DHCPv6" required> DHCPv6<br><br>

        <input type="submit" value="Request IP">
    </form>
</body>
</html>
