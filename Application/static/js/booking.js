document.querySelector("#dateIn").addEventListener("input", (e) => {
  var days = parseInt(document.querySelector("#days").value);
  var myDate = e.target.value;
  if (days) {
    var newDate = addDays(myDate, days);
    var formattedDate = newDate.split("/");
    dateOut = `${formattedDate[2]}-${formattedDate[0]}-${formattedDate[1]}`;
    document.querySelector("#dateOut").value = dateOut;
    console.log(dateOut);
    // var outDate = formartDate(newDate);
    // console.log(outDate);
  } else {
    document.querySelector(".notify").classList.add("notifying");
    document.querySelector(".notification").innerHTML =
      "Kindly enter days to proceeed";
    // document.querySelector("#days").addEventListener("input", (e) => {
    //   if (e) {
    //     document.querySelector(".notify").classList.remove("notifying");
    //     var date = document.querySelector("#dateIn").value;
    //     var noDays = e.target.value;
    //     var date = date;
    //     console.log(date);
    //     var newDate = addDays(date, noDays);
    //     console.log(newDate);
    //   }
    // });
  }
});
function addDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result.toLocaleDateString("en-US");
}
