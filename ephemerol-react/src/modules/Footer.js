/*
Copyright (C) 2016-Present Pivotal Software, Inc. All rights reserved.

 This program and the accompanying materials are made available under
 the terms of the under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/

import React from 'react';
import './App.css';

class Footer extends React.Component {

    render() {
        return (
            <div className="row footer">
                <p>Sponsored by <a href="http://pivotal.io">Pivotal Software, Inc.</a></p>
            </div>
        );
    }
}

export default Footer;

