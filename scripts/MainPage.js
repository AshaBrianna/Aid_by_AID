let total_elements = document.querySelectorAll(".total");
let urlParams = new URLSearchParams(window.location.search);
let budget= urlParams.get('student_budget');

for(let total_element of total_elements){
  let int_total = parseInt(total_element.dataset['total']);
  if(int_total <= budget){
      //make green
      total_element.classList.add("isInBudget");
  }
  else{
    //make red
    total_element.classList.add("isNotInBudget");
  }
}
$(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();
