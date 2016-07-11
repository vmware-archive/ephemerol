# .NET Framework Scanning
.NET app scanning will look at traditional Visual Studio created, C# .NET projects, and scan the configuration files and source files for potential issues.

## Configuration Files
* Checks to make sure .NET Framework version is 3.5, 4.*, otherwise reports a higher refactor rating depending on how far back from .NET 3.5 the app is.

## Source Files
* No use of Windows Service functionality to run (classes extending ServiceBase)
* Use of OLEDB, ODBC, ADO.NET or EntityFramework
* Warning on Local Filesystem access

##Proposed checks