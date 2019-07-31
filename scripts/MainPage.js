
let total_elements = document.querySelectorAll(".total");
let budget=globalBudget;

for(let total_element of total_elements){
  let int_total = parseInt(total_element.dataset['total']);
  if(int_total < budget){
      //make green
      total_element.classList.add("isInBudget");
  }
  else{
    //make red
    total_element.classList.add("isNotInBudget");
  }
}
