import paramiko

def block_websites(remote_host, username, password, websites):
    try:
        # Connect to the remote host
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(remote_host, port=22, username=username, password=password)

        # Define the hosts file path
        hosts_file_path = '/etc/hosts'  # Modify the path if it's different on your system

        # Read the existing hosts file
        stdin, stdout, stderr = ssh_client.exec_command('cat ' + hosts_file_path)
        existing_hosts = stdout.read().decode('utf-8')

        # Add blocked websites to the hosts file
        with ssh_client.open_sftp() as sftp:
            with sftp.file(hosts_file_path, 'a') as hosts_file:
                for website in websites:
                    hosts_file.write('\n127.0.0.1 ' + website)

        print("Websites blocked successfully.")

        # Close the SSH connection
        ssh_client.close()

    except Exception as e:
        print("An error occurred:", str(e))

# Replace these variables with your actual remote host details
remote_host = '192.168.68.117'
username = 'REMOTE_USERNAME'
password = 'REMOTE_PASSWORD'

# List of websites to block
websites_to_block = ['ynet.com', 'www.ynet.co.il']

block_websites(remote_host, username, password, websites_to_block)