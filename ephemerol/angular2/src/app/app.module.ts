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

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule }   from '@angular/router';

import { AppComponent } from './app.component';
import { GettingStartedComponent } from './setup/getting-started.component';
import { HelpHomeComponent } from './help/help-home.component';
import { ScannerCategoriesComponent } from './setup/scanner-categories.component';
import { NavbarTopComponent } from './navigation/navbar-top.component';

import { SourceUploadComponent } from './setup/source-upload.component';
import { RulesUploadComponent } from './setup/rules-upload.component';

@NgModule({
  declarations: [
    AppComponent,
    GettingStartedComponent,
    ScannerCategoriesComponent,
    NavbarTopComponent,
    SourceUploadComponent,
    RulesUploadComponent,
    HelpHomeComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    RouterModule.forRoot([
      { path: '', redirectTo: '/getting-started', pathMatch: 'full'},
      { path: 'getting-started', component: GettingStartedComponent },
      { path: 'help', component: HelpHomeComponent },
      { path: 'source-upload', component: SourceUploadComponent },
      { path: 'rules-upload', component: RulesUploadComponent }
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})

export class AppModule { }
