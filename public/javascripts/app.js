(function(){
  var app = angular.module('sudoku', ['ngSanitize']);

  app.controller('sudokuController', function($scope, $http, $interval){

    $scope.sukses = 1;
    $scope.squares = [];
    $scope.ukuran = 4;
    $scope.akar = 2;
    $scope.ukuran_cell = {};

    for (var i = 1; i <= 5; ++i) {
      $scope.squares.push(i*i);
      $scope.ukuran_cell[i*i] = (Math.min(40, Math.floor(1000/(i*i))));
      if( $scope.ukuran_cell[i*i] < 40 ) $scope.ukuran_cell[i*i] = 40;
    }

    $scope.changed = function(){
      $scope.ukuran = $scope.dropdown_ukuran ? $scope.dropdown_ukuran : 4;
      $scope.akar = Math.sqrt($scope.ukuran);
      $scope.m = [];
      for (var i = 0; i < $scope.ukuran; ++i) {
        var baris = [];
        for (var j = 0; j < $scope.ukuran; ++j) baris.push(0);
        $scope.m.push(baris);
      };
      $scope.$applyAsync();
    }

    $scope.changed();

    var beda = function(arr1, arr2)
    {
      if(arr1.length != arr2.length) return true;
      for (var i = 0; i < arr1.length; ++i) {
        if(arr1[i].length != arr2[i].length) return true;
        for (var j = 0; j < arr1[i].length; ++j) {
          if( arr1[i][j] != arr2[i][j] ) return true;
        }
      };
      return false;
    };

    var valid = function(arr){
      for (var i = 0; i < arr.length; ++i)
        for (var j = 0; j < arr[i].length; ++j)
        {
          if( parseInt(arr[i][j]) == NaN || parseInt(arr[i][j]) != parseFloat(arr[i][j]) ) return false;
          arr[i][j] = parseInt(arr[i][j]);
        }
      return true;
    }

    var arrayClone = function(arr) {
      return arr.slice(0).map(function(x){return x.slice(0);});
    };

    var pre_m = [];
    $scope.blocking = false;

    var resolve = function(){
      if($scope.blocking) return;
      if(valid($scope.m) && beda(pre_m, $scope.m))
      {
        pre_m = arrayClone($scope.m);
        $scope.blocking = true;
        $scope.s = [];
        $scope.terlihat = [];
        $http.post("/solve", $scope.m)
        .success(function(response){
          $scope.blocking = false;
          var splitted = response.trim().split("\n");
          var nsol = parseInt(splitted.shift());
          for(var i = 0; i < nsol; ++i)
          {
            $scope.s.push(
              splitted.splice(-$scope.ukuran)
              .map(function(baris){return baris.split(" ");})
            );
            if(i == 0) $scope.terlihat.push(1);
          };
        })
        .error(function(){
          $scope.blocking = false;
        });
      }
    };

    resolve();
    $interval(resolve, 500);

  });

})();
