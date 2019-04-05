var app = angular.module('whohascabin6598', []);
app.controller('submitTipsCtrl', function($scope, $http) {
    $scope.loading = false;
    $scope.sendTip = function() {

        var postData = {};
        postData.tipText = $scope.tipText;

        $scope.tipText = "";
        $scope.loading = true;

        $http.post('https://us-central1-ajnhosting-163818.cloudfunctions.net/add-anonymous-tip', postData, {})
            .then(postSuccess, errorCallback);

    };

    function postSuccess() {
        $scope.loading = false;
    }

    function errorCallback() {
        $scope.loading = false;
        return false;
    }

});

app.controller('tipsCtrl', function($scope, $http, $interval) {
    $scope.tips = [];
    getTips();

    function getTips() {
        $http({
            method: 'GET',
            url: 'https://storage.googleapis.com/cabin-6598-tips/tips.json'
        }).then(function successCallback(response) {
            processTips(response)
        }, errorCallback);
    }

    function processTips(response) {
        $scope.tips = response.data.tips;
        for (var i = 0; i < $scope.tips.length; i++) {
          var date = new Date($scope.tips[i].timestamp + ' UTC');
          $scope.tips[i].timestamp = date.toLocaleString();
        }
    }

    $interval(getTips, 1000);

});

function errorCallback() {
    return false;
}
