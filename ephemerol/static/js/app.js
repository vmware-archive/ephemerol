(function () {
    var app = angular.module('pad', [])

    app.config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }]);

    app.controller('Controller', ['$http', '$scope', function ($http, $scope) {

        var svc_response = this;

        this.callSomething = function () {
            svc_response.result = null;
            $http.get('/analyze').success(function (data) {
                    svc_response.result = data;
            }).error(function (data, status, headers, config) {
                    svc_response.result = data;
            });

        };

    }]);

})();