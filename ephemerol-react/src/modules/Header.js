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
import request from 'superagent';

class Header extends React.Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.updateScanStats = this.updateScanStats.bind(this);
        this.rulesLoad = this.rulesLoad.bind(this);
        this.state = {message: null, error: null};
    }

    handleSubmit(event) {
        event.preventDefault();
        var file = document.getElementById('upload-file-selector').files[0];
        this.props.addFileName(file.name);
        var formData = new FormData();
        formData.append('file', file);

        if (file.name.endsWith(".zip")) {
            request
                .post('/scan')
                .send(formData)
                .set('Accept', 'application/json')
                .end(this.updateScanStats);
        }
        if (file.name.endsWith(".yml")) {
            request
                .post('/load_rules')
                .send(formData)
                .set('Accept', 'application/json')
                .end(this.rulesLoad);
        }
        else{
            this.setState({error: "Only YML rule sets or ZIP source files can be uploaded", message: null});
        }
    }

    updateScanStats = function (err, res) {
        if (err) {
            this.setState({error: "File Scan Error", message: null});
        }
        else {
            this.props.addScanStats(true, res.body.scan_stats);
            this.setState({message: "Successful File Scan", error: null});
        }
    };

    rulesLoad = function (err, res) {
        if (err) {
            this.setState({error: "Rule Load Error", message: null});
        }
        else {
            this.setState({message: "Successful Rules Upload", error: null});
        }
    };

    render() {
        let message = null;
        let error = null;
        if (this.state.message != null) {
            message = <div className="fa fa-2x fa- fa-info-circle fa-h4"> {this.state.message}</div>
        }
        if (this.state.error != null) {
            error = <div className="fa fa-2x fa-exclamation-circle fa-h4"> {this.state.error}</div>
        }
        return (
            <div>
                <div className="row">
                    <div className="col-md-9">
                        <h2 className="">
                            <a href="/" className="logo-text"><span>Ephemerol</span></a>
                        </h2>
                        {message}
                        {error}
                    </div>
                    <div className="col-md-3 pull-right">
                        <div>
                            <form id="scan_form" method="post" encType="multipart/form-data"
                                  role="form"
                                  className="form-inline top-buffer" onSubmit={this.handleSubmit}>
                                <div className="form-group">
                                    <span id="fileselector">
                                        <label className="btn btn-default" for="upload-file-selector">
                                            <input id="upload-file-selector" type="file" name="file"/>
                                            <i className="better-font fa fa-upload btn btn-primary fa-2x"></i>
                                        </label>
                                    </span>
                                </div>
                                <div className="form-group">
                                    <button type="submit" name="submitbtn" className="btn btn-primary fa-2x"
                                            value="zip_scan">Upload
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <hr className="header"></hr>
            </div>
        );
    }
}

export default Header;
