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

import {Injectable}     from '@angular/core';
import {Http, Response} from '@angular/http';
import {Observable}     from 'rxjs/Observable';

export class Rule {
  constructor(public app_type:string,
              public description:string,
              public file_type:string,
              public file_name:string,
              public text_pattern:string,
              public file_category:string,
              public refactor_rating:number) {
  }
}

@Injectable()
export class RuleLoadService {
  private ruleLoadUrl = 'http://localhost:5000/upload/default';  // URL to web API

  constructor(private http:Http) {
  }

  getDefaultRules():Observable<Rule[]> {

    return this.http.get(this.ruleLoadUrl).map(this.extractData).catch(this.handleError);
  }

  private extractData(res:Response) {
    alert('bbb')
    return res || {};
  }

  private handleError(error:Response | any) {

    // In a real world app, we might use a remote logging infrastructure
    let errMsg:string;
    if (error instanceof Response) {
      const body = error.json() || '';
      const err = body.error || JSON.stringify(body);
      errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
    } else {
      errMsg = error.message ? error.message : error.toString();
    }
    console.error(errMsg);
    return Observable.throw(errMsg);
  }
}
