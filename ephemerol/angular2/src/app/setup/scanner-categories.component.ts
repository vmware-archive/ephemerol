import {Component, Input} from '@angular/core';
@Component({
  selector: 'scanner-categories',
  template: `
    <div class='row' style="margin-top: 50px;">
        <div class="col-md-4">
            <div class="panel panel-info">
                <div class="panel-heading">
                    Java
                </div>
                <div class="panel-body">
                    <p style="height: 50px;">Application server dependencies, JEE API use and hard-coded
                        configuration files</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="panel panel-info">
                <div class="panel-heading">
                    .NET
                </div>
                <div class="panel-body">
                    <p style="height: 50px;">Check for .NET Core and hard-coded
                        configuration files</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="panel panel-info">
                <div class="panel-heading">
                    Other
                </div>
                <div class="panel-body">
                    <p style="height: 50px;">Check for 12 Factor violations and other cloud readiness issues</p>
                </div>
            </div>
        </div>
    </div>
  `
})
export class ScannerCategoriesComponent {

}
