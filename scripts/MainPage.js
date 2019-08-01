
let total_elements = document.querySelectorAll(".total");
let budget=globalBudget;
let grants = globalGrants;

for(let total_element of total_elements){
  let int_total = parseInt(total_element.dataset['total']);
  int_total -= grants;
  if(int_total < budget){
      //make green
      total_element.classList.add("isInBudget");
  }
  else{
    //make red
    total_element.classList.add("isNotInBudget");
  }
}
