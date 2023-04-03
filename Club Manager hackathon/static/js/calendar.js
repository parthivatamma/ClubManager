//makeCalendar()
function makeCalendar(){
  var calendar = document.getElementById("calendar");
  var calHtml = `
  <div class="border border-light rounded container">
    <table class = "table table-dark table-hover">
    <tr>
        <th>Hours</th>
        <th>Sunday</th>
        <th>Monday</th>
        <th>Tuesday</th>
        <th>Wednesday</th>
        <th>Friday</th>
        <th>Saturday</th>
    </tr>
   </div>
    `
  var ampm = ""
  for (let i = 0; i < 24; i++){
    if (i <12)
      ampm ="A.M."
    else
      ampm = "P.M."
    calHtml+=`
    <tr>
      <td>`+i+`:00 `+ampm+`</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
   </tr>`
  }  
  calHtml+="</table>"
  calendar.innerHTML = calHtml
  console.log(calHtml)
}

// $(".toggle").click(function () {
//   $(".navigation").toggleClass("active");
// });

// $(".theme").click(function () {
//   $(".theme").removeClass("select");
//   $(this).addClass("select");
// });

// $(".dark").click(function () {
//   $("body").removeClass("lighted");
//   $("body").removeClass("purpled");
//   $("body").addClass("darked");
// });

// $(".light").click(function () {
//   $("body").removeClass("purpled");
//   $("body").removeClass("darked");
//   $("body").addClass("lighted");
// });

// $(".purple").click(function () {
//   $("body").removeClass("lighted");
//   $("body").removeClass("darked");
//   $("body").addClass("purpled");
// });