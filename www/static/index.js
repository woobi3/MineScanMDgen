function copy() {
  var copyText = document.getElementById("ip");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard
    .writeText(copyText.value)
    .then(() => {
      alert("successfully copied");
    })
    .catch(() => {
      alert("something went wrong");
    });
}

function graph() {
  let x = [];
  for (let i = 0; i < 4; i++) {
    x[i] = i;
  }

  let sot = {
    y: x,
    type: 'bar',
    name: 'servers over time',
  };
  let sotdata = [sot];

  let sotlayout = {
    plot_bgcolor: "rgb(0,0,0)",
    paper_bgcolor: "rgb(0,0,0)",
    showbackground: true,
  }

  Plotly.newPlot('sot', sotdata, sotlayout, {staticPlot: true});
}




window.onload=()=>{
  graph();
};