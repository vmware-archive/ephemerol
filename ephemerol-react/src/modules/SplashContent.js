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
import ReactImg from '../images/react-logo.svg';
import YamlImg from '../images/yaml.png';

class SplashContent extends React.Component {

    render() {
        return (
            <div>

                <div className="row content">
                    <div>
                        <h1>Source Code Scanner</h1>
                        <h2>Upload source .ZIP to conduct cloud readiness
                            checks</h2>
                    </div>
                    <div className="section">
                        <div className="section_part">
                            <h3>JAVA</h3>
                            <p> Application server dependencies, JEE API use and hard-coded
                                configuration files</p>
                        </div>
                        <div className="section_part"><h3>.NET</h3>
                            <p>
                                Check for .NET Core and hard-coded
                                configuration files
                            </p>
                        </div>
                        <div className="section_part"><h3>OTHER</h3><p>
                            Check for 12 Factor violations and other cloud readiness issues
                        </p>
                        </div>
                    </div>
                </div>
                <div>
                    <div className="content_row">
                        <div className="content_col">
                            <h2 >Configurable and Simple</h2>
                            <p>YAML based configuration that is easy to customize. Glorified grep for all source and
                                config
                                files. We will find most of your cloud native issues.</p>
                        </div>
                        <div className="content_col">
                            <img src={YamlImg}/>
                        </div>
                    </div>
                </div>
                <div className="alt_bg">
                    <div className="content_row">
                        <div className="content_col">
                            <img src={ReactImg} className="react-logo"/>
                        </div>
                        <div className="content_col">
                            <h2>Slick User Interface</h2>
                            <p>Upload a ZIP file of your source code and the user interface will display summarized
                                and detailed cloud readiness reports.</p>
                        </div>
                    </div>
                </div>
                <div>
                    <div className="content_row">

                        <div className="content_col">
                            <h2>CI/CD Tool Integration</h2>
                            <p>Invoke ephemerol from the command line and the scanner rules will run and pretty print in <a href="http://concourse.ci">Concourse</a> or a less capable continous integration tool.</p>
                        </div>
                        <div className="content_col">
                            <p className="cmd-example">python -m ephemerol rulefile.yml source.zip</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default SplashContent;
