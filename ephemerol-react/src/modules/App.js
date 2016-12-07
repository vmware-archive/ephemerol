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
import SplashContent from './SplashContent';
import Header from './Header.js';
import Footer from './Footer.js';
import './App.css';
import ScanStats from './ScanStats.js';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {showScanOutput: false, scan_stats: [], fileName: ""};
        this.addScanStats = this.addScanStats.bind(this);
        this.addFileName = this.addFileName.bind(this);
    }

    addScanStats(showFlag, responseBody) {
        this.setState({scan_stats: responseBody, showScanOutput: showFlag});
    }

    addFileName(fileName) {
        this.setState({fileName: fileName});
    }

    render() {
        let body = null;
        if (this.state.showScanOutput) {
            body = <ScanStats scan_stats={this.state.scan_stats} fileName={this.state.fileName}/>;
        } else {
            body = <SplashContent />;
        }

        return (
            <div className="container-fluid">
                <Header addScanStats={this.addScanStats} addFileName={this.addFileName}/>
                {body}
                <Footer/>
            </div>
        );
    }
}

export default App;
