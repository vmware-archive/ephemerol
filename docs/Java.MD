# Java Scanning
Java project scanning looks for the presence of Web, Java EE, and Application server specific configuration files, as well as class imports which might be problematic for an app running in light-weight containers.
## Configuration Files
The rulebase currently checks for Java Web Profile deployment descriptors, Java EE deployment descriptors, and deployment descriptors for IBM WebSphere, Oracle WebLogic, and RedHat JBoss Application server.

Additionally, the scanner looks for XML configuration files that contain references to port settings, as well as references to specific file:// URLs.