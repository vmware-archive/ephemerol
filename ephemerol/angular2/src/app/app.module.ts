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
