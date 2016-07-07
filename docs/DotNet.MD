# .NET Framework Scanning
.NET app scanning will look at traditional Visual Studio created .NET projects, and scan the configuration files and source files for potential issues.

##Proposed checks
* .NET Framework version is 3.5, 4.*
* No use of Windows Service functionality to run
* Warning on Local Filesystem access
* Use of ADO.NET or EntityFramework