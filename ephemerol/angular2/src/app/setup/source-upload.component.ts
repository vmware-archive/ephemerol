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

import { Component, OnInit } from '@angular/core';
import { RuleLoadService, Rule } from './rules-load.service';
@Component({
  selector: 'source-upload',
  providers: [RuleLoadService],
  template: `
   <div class="row">
        <div class="col-lg-12">
            <h1 class="page-header">Get Started</h1>
        </div>
    </div>
    <div class="panel panel-default">
        <div class="panel-heading">
            Step #2 - Upload/Scan Source Code
        </div>
        <div class="panel-body">
           <h1>TODO - FILE UPLOAD!!!!</h1>
        </div>
        <div class="panel-footer">
            Click "Default" if this is your first time
        </div>
    </div>
  `
})
export class SourceUploadComponent implements OnInit {

   errorMessage: string;
   rules: Rule[];
   mode = 'Observable';

  constructor(
    private service: RuleLoadService
  ) {}

  ngOnInit() {
    this.service.getDefaultRules();
  }

}
