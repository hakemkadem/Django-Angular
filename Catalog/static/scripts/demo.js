var myApp = angular.module("myApp", []);

myApp.config(function($interpolateProvider) {
$interpolateProvider.startSymbol('[[');
$interpolateProvider.endSymbol(']]');
});

myApp.controller("MyController", ["$scope","$location","$http", function($scope, $location, $http) {
$scope.myName = "Hakim Adil Will Win in Django";
$scope.GetData=function(item){
 $http.get('validate_username/',
                       { params: { 'authName': item}
                       }).success(function (data) {
                          $scope.DatedVault= data;

                       }).error(function (error, status) {

                       });
                       };
}]);