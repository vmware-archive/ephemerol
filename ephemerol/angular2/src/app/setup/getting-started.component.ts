// Copyright (C) 2016-Present Pivotal Software, Inc. All rights reserved.
//
// This program and the accompanying materials are made available under
// the terms of the under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import {Component, Input} from '@angular/core';
@Component({
  selector: 'getting-started',
  template: `
   <scanner-categories></scanner-categories>
   <div class="row">
        <div class="col-lg-12">
            <h1 class="page-header">Get Started</h1>
        </div>
    </div>
    <div class="panel panel-default">
        <div class="panel-heading">
            Step #1 - Load YAML Rule Base
        </div>
        <div class="panel-body">
            <div class="col-md-6">
                <div class="panel">
                     <p style="text-align: center" >Newbie</p>
                    <a href="/source-upload"
                            class="btn btn-primary btn-lg btn-block huge"><i class="fa fa-file-text-o"></i> Default
                    </a>
                </div>
            </div>
            <div class="col-md-6">
                <div class="panel">
                    <p style="text-align: center" >Expert</p>
                    <a href="/rules-upload" 
                        class="btn btn-primary btn-lg btn-block huge"><i class="fa fa-file-code-o"></i> Custom
                    </a>
                </div>
            </div>
        </div>
        <div class="panel-footer">
            Click "Default" if this is your first time
        </div>
    </div>
  `
})
export class GettingStartedComponent {

}
