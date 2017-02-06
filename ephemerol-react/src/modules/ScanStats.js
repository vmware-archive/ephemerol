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

class ScanItem extends React.Component {
    render() {
        return (
            <tr>
                <td>{this.props.scan_item.app_type}</td>
                <td>{this.props.scan_item.file_category}</td>
                <td>{this.props.scan_item.file_type}</td>
                <td>{this.props.scan_item.flagged_file_id}</td>
                <td>{this.props.scan_item.refactor_rating}</td>
                <td>{this.props.scan_item.description}</td>
                <td>{this.props.scan_item.replatform_advice}</td>
            </tr>
        )
    }
}

class ScanStats extends React.Component {
    render() {

        var scan_items = this.props.scan_stats.scan_items.map(scan_item =>
            <ScanItem scan_item={scan_item}/>
        );
        var scan_items_info = this.props.scan_stats.scan_items_info.map(scan_item =>
            <ScanItem scan_item={scan_item}/>
        );
        return (
            <div>
                <div className="row scanContent">
                    <div>
                         <h1>{this.props.fileName}</h1>
                    </div>
                    <div className="section">
                        <div className="scan_stats_part">
                            <h2>{this.props.scan_stats.cloud_readiness_index}</h2>
                            <p>Cloud Readiness Index</p>
                        </div>
                        <div className="scan_stats_part">
                            <h2>{this.props.scan_stats.categories_flagged}</h2>
                            <p>Categories Flagged</p>
                        </div>
                        <div className="scan_stats_part">
                            <h2>{this.props.scan_stats.files_flagged}</h2>
                            <p>Files Flagged</p>
                        </div>
                        <div className="scan_stats_part">
                            <h2>{this.props.scan_stats.total_results}</h2>
                            <p>Total Results</p>
                        </div>
                    </div>
                </div>
                <div className="table-responsive">
                    <h2>Problem Files</h2>
                    <table className="table table-bordered">
                        <tbody>
                        <tr>
                            <th>App Type</th>
                            <th>File Category</th>
                            <th>File Type</th>
                            <th>File Path</th>
                            <th>Refactor Rating</th>
                            <th>Description</th>
                            <th>Replatform Advice</th>
                        </tr>
                        {scan_items}
                        </tbody>
                    </table>
                    <h2>Informational Items</h2>
                    <table className="table table-bordered">
                        <tbody>
                        <tr>
                            <th>App Type</th>
                            <th>File Category</th>
                            <th>File Type</th>
                            <th>File Path</th>
                            <th>Refactor Rating</th>
                            <th>Description</th>
                            <th>Replatform Advice</th>
                        </tr>
                        {scan_items_info}
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
}
export default ScanStats;