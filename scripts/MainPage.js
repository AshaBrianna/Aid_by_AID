let total_elements = document.querySelectorAll(".total");
let budget = document.querySelctorAll("");
for(let total_element of total_elements){
  let int_total = parseInt(total_element.dataset['total']);
  if(int_total < budget){
      //make green
      total_element.classList.add("isInBudget");
  }
  else{
    total_element.classList.add("isNotInBudget");
  }
}
$(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();
