Installing a GoDaddy SSL certificate on an AWS Ubuntu server involves several steps, including generating a Certificate Signing Request (CSR), obtaining the SSL certificate from GoDaddy, and configuring your server to use the certificate. Here’s a step-by-step guide:

### 1. Generate a Certificate Signing Request (CSR)

1. **SSH into your AWS Ubuntu server:**

   ```bash
   ssh username@your-server-ip
   ```

2. **Generate a private key and CSR:**

   ```bash
   openssl req -newkey rsa:2048 -nodes -keyout /etc/ssl/private/your_domain.key -out /etc/ssl/certs/your_domain.csr
   ```

   Replace `your_domain` with your actual domain name.

   - You will be prompted to enter details for your certificate:
     - Country Name (2 letter code)
     - State or Province Name
     - Locality (City)
     - Organization Name
     - Organizational Unit (Optional)
     - Common Name (your domain name, e.g., www.example.com)
     - Email Address

3. **Submit the CSR to GoDaddy:**

   - Log in to your GoDaddy account.
   - Go to the "My Products" page.
   - Find your SSL certificate and click "Manage".
   - Click "Re-key Certificate" or "New CSR", and paste your CSR content.
   - GoDaddy will process your request and provide you with the SSL certificate files.

### 2. Download and Install the SSL Certificate

1. **Download your SSL certificate files from GoDaddy:**

   You will typically get a zip file containing:
   - Your domain certificate (`your_domain.crt`)
   - Intermediate certificates (often named `gd_bundle-g2-g1.crt` or similar)

2. **Upload the SSL certificate files to your server:**

   Use SCP, SFTP, or any file transfer method to upload the files to your server, usually in `/etc/ssl/certs` or `/etc/ssl/private`.

3. **Install the SSL certificate:**

   **For Apache:**

   - Open the Apache configuration file or virtual host file where you want to configure SSL. This file is often located in `/etc/apache2/sites-available/` or `/etc/apache2/sites-enabled/`.

     ```bash
     sudo nano /etc/apache2/sites-available/your_domain.conf
     ```

   - Add or modify the following lines to include your certificate files:

     ```apache
     <VirtualHost *:443>
         ServerAdmin webmaster@your_domain
         ServerName your_domain
         DocumentRoot /var/www/html

         SSLEngine on
         SSLCertificateFile /etc/ssl/certs/your_domain.crt
         SSLCertificateKeyFile /etc/ssl/private/your_domain.key
         SSLCertificateChainFile /etc/ssl/certs/gd_bundle-g2-g1.crt

         <Directory /var/www/html>
             AllowOverride All
         </Directory>

         ErrorLog ${APACHE_LOG_DIR}/error.log
         CustomLog ${APACHE_LOG_DIR}/access.log combined
     </VirtualHost>
     ```

   - Enable the SSL module and the new site configuration:

     ```bash
     sudo a2enmod ssl
     sudo a2ensite your_domain.conf
     ```

   - Restart Apache to apply changes:

     ```bash
     sudo systemctl restart apache2
     ```

   **For Nginx:**

   - Open the Nginx configuration file for your site, typically found in `/etc/nginx/sites-available/` or `/etc/nginx/sites-enabled/`.

     ```bash
     sudo nano /etc/nginx/sites-available/your_domain
     ```

   - Add or modify the following lines in your server block:

     ```nginx
     server {
         listen 443 ssl;
         server_name your_domain;

         ssl_certificate /etc/ssl/certs/your_domain.crt;
         ssl_certificate_key /etc/ssl/private/your_domain.key;
         ssl_trusted_certificate /etc/ssl/certs/gd_bundle-g2-g1.crt;

         root /var/www/html;
         index index.html index.htm;

         location / {
             try_files $uri $uri/ =404;
         }
     }
     ```

   - Restart Nginx to apply changes:

     ```bash
     sudo systemctl restart nginx
     ```

### 3. Verify the Installation

1. **Check the SSL certificate installation:**

   - Use an SSL checker tool, such as [SSL Labs' SSL Test](https://www.ssllabs.com/ssltest/), to verify that your SSL certificate is installed correctly and is trusted.

2. **Ensure that your server is serving content over HTTPS properly.**

By following these steps, you should have successfully installed and configured your GoDaddy SSL certificate on your AWS Ubuntu server. If you encounter any issues, checking server logs or the SSL certificate’s validity and chain can help troubleshoot.