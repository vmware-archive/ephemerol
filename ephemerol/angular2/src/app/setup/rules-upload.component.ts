import { Component, Input } from '@angular/core';
@Component({
  selector: 'rules-upload',
  template: `
   <div class="row">
        <div class="col-lg-12">
            <h1 class="page-header">Get Started</h1>
        </div>
    </div>
    <div class="panel panel-default">
        <div class="panel-heading">
            Step #1 - Upload YAML Rule Base
        </div>
        <div class="panel-body">
           <h1>TODO - FILE UPLOAD!!!!</h1>
        </div>
        <div class="panel-footer">
            Click "Default" if this is your first time
        </div>
    </div>
    <div ng-hide="scanner-categories"></div>
  `
})
export class RulesUploadComponent {

}
