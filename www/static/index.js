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
  };
  let sotdata = [sot];
  let sotlayout = {
  colorway:[ '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff']  
  }

  Plotly.newPlot('sot', sotdata);
}




window.onload=()=>{
  graph();
};