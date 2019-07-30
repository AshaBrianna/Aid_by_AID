const putTotal = document.querySelector("#total")


  var housing = document.getElementById("housing").value;
  var food = document.getElementById("food").value;
  var tuition = document.getElementById("tuition").value;
  // var travel = document.getElementById("travel").value;
  var total = housing + food + tuition + travel;
  putTotal.innerHTML = "Total: " + total;

  console.log(housing, food, tuition, travel, total);
