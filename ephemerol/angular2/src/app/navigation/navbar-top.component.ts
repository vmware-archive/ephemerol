import {Component, Input} from '@angular/core';
@Component({
  selector: 'navbar-top',
  template: `
   <div id="wrapper">
    <!-- Navigation -->
    <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
        <div class="navbar-header">
            <a class="navbar-brand" href="index.html">Ephemerol - Source Code Scanner</a>
        </div>
        <ul class="nav navbar-top-links navbar-right">
            <li>
                <a class="dropdown-toggle" data-toggle="dropdown" href="/">
                    Getting Started
                </a>
            </li>
            <li class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="/help">
                    Help
                </a>
            </li> 
        </ul>
    </nav>
</div>
  `
})
export class NavbarTopComponent {

}
