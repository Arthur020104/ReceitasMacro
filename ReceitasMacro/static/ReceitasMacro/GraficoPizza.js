import 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.8.0/chart.min.js';

export function criapizza(dado,elementappend)
{
  for(let i = 0; i < dado.length;i++)
  {
    dado[i] = dado[i].toFixed(2)
  }
  //const Chart = require('chart.js');
  let canvas = document.createElement('canvas');
  let title = document.createElement('h3');
  elementappend.appendChild(title);
  title.classList.add('title-full','text-center', 'gray')
  title.innerHTML = 'Distribuição de calorias por Macronutriente';
  canvas.id = "myChart";
  elementappend.appendChild(canvas);
  let ctx = document.getElementById('myChart').getContext('2d'); 

  let chartGraph = new Chart(ctx,{
    type:'pie',
    data:{
      labels: ['Carboidratos','Proteínas','Gorduras'],
      datasets:[{
        label: 'Calorias por Macro',
        data: dado,
        borderColor:'transparent',
        backgroundColor: [
          'rgb(77, 77, 186)',
          'rgb(200, 255, 9)',
          'rgb(253, 200, 9)'
        ],
        hoverOffset: 4,
        
      }]
    }
  } );
}