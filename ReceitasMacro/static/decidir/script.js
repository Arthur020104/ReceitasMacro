import {criapizza} from './GraficoPizza.js'
import {click} from './click.js'
function cardbtn(cards_btn)
{
  cards_btn.forEach(card=>
    {
      card.addEventListener("click",()=>
      {
        let id = card.dataset.id_receita;
        fetch('/info/receita/'+id)
        .then(response => response.json())
        .then(receita => {
          // Print receita
          // console.log(receita);
          if("error" in receita)
          {
            alert(receita);
          }
          fullpage(receita)
        });
      });
    });
}
function fullpage(receita)
{
  let busca = document.getElementById("busca-form");
  let x = document.getElementById("carousel1");
  if(x)
  {
    x.remove();
  }
  if(busca)
  {
    busca.style.display = "none";
  }
  let separation_border = document.querySelector('.separation_border');
  if(separation_border)
  {
    document.querySelector('.separation_border').style.display = 'none';
  }
  document.querySelector('#receitas').style.display = 'none';
  let fullpage = document.querySelector('#fullpage');
  fullpage.style.display = 'block';
  let container_page = document.createElement('div');
  let ingredientes = document.createElement('section');
  let modopreparo = document.createElement('section');
  fullpage.appendChild(container_page);
  fullpage.appendChild(ingredientes);
  fullpage.appendChild(modopreparo);

  modopreparo.classList.add("container");
  ingredientes.classList.add("container");
  container_page.classList.add("container");

  let carousel = '<div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel"><ol class="carousel-indicators">';
  for(let i = 0; i < receita.img.length; i++)
  {
    if(i == 0)
    {
      carousel += '<li data-target="#carouselExampleIndicators" data-slide-to="'+i+'" class="active"></li>';
    }
    else
    {
      carousel += '<li data-target="#carouselExampleIndicators" data-slide-to="'+i+'"></li>';
    }
    if(i == (receita.img.length-1))
    {
      carousel += '</ol>';
      carousel += '<div class="carousel-inner">';
      for(let j = 0; j < receita.img.length; j++)
      {
        if(j==0)
        {
          carousel += '<div class="carousel-item active"><img src="'+receita.img[j]+'" class="d-block w-100" alt="'+receita.name+'"></div>';
        }
        else
        {
          carousel += '<div class="carousel-item"><img src="'+receita.img[j]+'" class="d-block w-100" alt="'+receita.name+'"></div>';
        }
      }
      carousel += '</div>';
      carousel += '<button class="carousel-control-prev" type="button" data-target="#carouselExampleIndicators" data-slide="prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span><span class="sr-only">Previous</span></button><button class="carousel-control-next" type="button" data-target="#carouselExampleIndicators" data-slide="next"><span class="carousel-control-next-icon" aria-hidden="true"></span><span class="sr-only">Next</span></button></div>';
    }
  }

  container_page.innerHTML= "<div class='recipe-info text-center'><h3 class='title-full text-center color'>"+receita.name+"</h3>"+carousel+"<div class='row row-full'><div class='col-sm-2 coluna-full'><p class='text-center color'>Calorias</p><p class='text-center'>"+Number((receita.calorias).toFixed(1))+"</p></div><div class='col-sm-2 coluna-full'><p class='text-center color'>Carboidratos</p><p class='text-center'>"+Number((receita.carboidratos).toFixed(1))+"g</p></div><div class='coluna-full col-sm-2'><p class='text-center color'>Proteínas</p><p class='text-center'>"+Number((receita.proteinas).toFixed(1))+"g</p></div><div class='coluna-full col-sm-2'><p class='text-center color'>Gorduras</p><p class='text-center'>"+Number((receita.gorduras).toFixed(1))+"g</p></div><div class='coluna-full col-sm-2'><p class='text-center color'><i  class='fa-solid fa-heart like color'></i></p><p class='text-center'>"+receita.likes+"</p></div></div></div>";
  ingredientes.innerHTML = "<div class='ingrdients-info text-center'><h3 class='title-full text-center color'>Ingredientes <i class='fa-solid fa-cart-shopping color'></i></h3><p class='text-center text'>"+receita.ingredientes+"</p></div>";
  modopreparo.innerHTML = "<div class='ingrdients-info text-center'><h3 class='title-full text-center color'>Modo de preparo<i class='fa-solid fa-kitchen-set'></i></h3><p class='text-center text'>"+receita.modoPreparo+"</p></div>";
  if(localStorage.getItem("mode")=="dark")
  {
    darkfull();
  }
  let elemento = document.createElement('div');
  elemento.classList.add('canvas');
  let recipe_info = document.querySelector('.recipe-info');
  recipe_info.appendChild(elemento);
  criapizza([receita.carboidratos*4,receita.proteinas*4,receita.gorduras*9],elemento);
  document.getElementById('Logo').scrollIntoView({behavior: "smooth"});
}
export function alert(message)
{
  let alerts = document.createElement("div");
  alerts.style.transition = '1.2s ease all';
  let temp;
  if("error" in message)
  {
    alerts.classList.add('alert-danger', "alert");
    alerts.innerHTML = message['error'];
    alerts.animationDuration = 4000;
    temp = 5000;
  }
  else if("warning" in message)
  {
    alerts.classList.add('alert-warning', "alert");
    alerts.innerHTML = message['warning'];
    alerts.animationDuration = 4000;
    temp = 5000;
  }
  else if("loading" in message)
  {
    alerts.classList.add('alert-loding', "alert");
    alerts.innerHTML = message['loading'];
    alerts.animationDuration = 4000;
    temp = 5000;
  }
  else
  {
    alerts.classList.add('alert-success', "alert");
    alerts.innerHTML = message['message'];
    alerts.animationDuration = 3000;
    temp = 4000;
  }


  document.querySelector('#alert').appendChild(alerts);

  alerts.style.animationPlayState = 'running';
  setTimeout(() =>
  {
    alerts.style.animationName = "hidealert";
    alerts.style.animationPlayState = 'running';
    alerts.addEventListener("animationend",()=>
    {
      alerts.remove();
    })
  }, temp);
}
document.addEventListener('DOMContentLoaded',()=>{
let messagem = document.getElementById('minhareceitamsg');
if(messagem)
{
  window.history.pushState('', 'New Page Title', '/MinhasReceitas');
}
let busca = document.getElementById("busca");
if(busca)
{
  busca.addEventListener("keyup",function buscar(){
    let e = document.querySelector(".dropdown");
    let filtro = e.options[e.selectedIndex].value;
    let dropdown = document.querySelector(".dropdown");

    dropdown.addEventListener('change',()=>
    {
      buscar();
    });
    fetch('/busca',
    {
      method : 'POST',
      body: JSON.stringify(
      {
        content: busca.value,
        filtro: filtro
      })
    })
    .then(response => response.json())
    .then(result =>
    {
      let parent = document.getElementById('parent');
      parent.innerHTML = '';
      let counter = 0;
      let contentdis = document.createElement('div');
      contentdis.classList.add('row');
      let x = contentdis;
      //results in result
      for(let i = 0; i < result.length;i++)
      {
        let results = i;
        counter++;
        if(counter % 3 == 0)
        {
          parent.appendChild(x);
          let row = document.createElement('div');
          row.classList.add('row');
          x = row;
        }
        if(localStorage.getItem("mode")=="dark")
        {
          x.innerHTML += '<div class="col-lg-3"><div class="card" style="width: 18rem;"><img data-id_receita="'+result[results].id+'" class="card-img cards_btn" src="'+result[results].img[0]+'" alt='+result[results].name+'><div class="card-body dark-mode-body"><h5 data-id_receita="'+result[results].id+'" class="card-title cards_btn">'+result[results].name+'</h5></div></div></div>';
        }
        else
        {
          x.innerHTML += '<div class="col-lg-3"><div class="card" style="width: 18rem;"><img data-id_receita="'+result[results].id+'" class="card-img cards_btn" src="'+result[results].img[0]+'" alt='+result[results].name+'><div class="card-body"><h5 data-id_receita="'+result[results].id+'" class="card-title cards_btn">'+result[results].name+'</h5></div></div></div>';
        }
      }
      parent.appendChild(x);
      let cards_btn = document.querySelectorAll(".cards_btn");
      cardbtn(cards_btn);
    });
    });
}

let darkmode = document.querySelector("#darkmode");
function dark()
{
  let icons = document.querySelectorAll('button.icon');
  icons.forEach(icon =>{
    icon.classList.toggle('button-dark-mode');
  });
  const separation_border = document.querySelector(".separation_border");
  if(separation_border)
  {
    document.querySelector(".separation_border").classList.toggle('separation_border-dark-mode');
  }
  document.querySelector(".navbar-toggler").classList.toggle('toggler-icon-dark');
  document.querySelectorAll('.btn').forEach(btn =>{
    btn.classList.toggle('button-dark-mode');
  });
  document.querySelectorAll('.card-body').forEach(card =>{
    card.classList.toggle('dark-mode-body');
  });
  document.querySelectorAll('.title').forEach(title =>{
    title.classList.toggle('dark-nav');
  });
  document.querySelectorAll('.nav-item').forEach(item =>{
    item.classList.toggle('dark-nav');;
  });
  document.querySelectorAll('.form-control').forEach(form_control =>{
    form_control.classList.toggle('textarea-dark');;
  });

  document.querySelectorAll('.page-link').forEach(btn =>{
    	btn.classList.toggle('page-link-dark-mode');
  });
  document.querySelector('body').classList.toggle('dark-mode-body');
  document.querySelector('nav').classList.toggle('dark-mode-nav');
  document.getElementById('footer').classList.toggle('dark-mode-body');
  let img = document.getElementById("imgfooter")
  let recipefull = document.querySelector('.recipe-info')
  if(localStorage.getItem("mode")=="dark")
  {
    img.src = "https://live.staticflickr.com/65535/52005494254_36941ac353_m.jpg";
    localStorage.setItem("mode", "light");
    if(recipefull)
    {
      darkfull();
    }
  }
  else
  {
    localStorage.setItem("mode", "dark");
    img.src = "https://live.staticflickr.com/65535/52019582566_81ba0ca97d_m.jpg";
    if(recipefull)
    {
      darkfull();
    }
  }
}

darkmode.addEventListener('click',dark);

if(localStorage.getItem("mode")=="dark")
{
  localStorage.setItem("mode", "light");
  dark();
}



let message = document.getElementById("message")
if (message)
{
  alert({"error":message.innerHTML})
}

  let recipebtn = document.querySelector("#recipe-make");

  if (recipebtn)
  {
    let content = document.querySelector("#ingred");
    
  }
  let btn_tradutor = document.getElementById('btn_traduzir');
  if(btn_tradutor)
  {
    btn_tradutor.addEventListener('click', ()=>
    {
      let content = document.querySelector("#ingred");
      fetch('/tradutor',
      {
        method : 'POST',
        body: JSON.stringify(
        {
          traduzir: content.value,
          lang: "en"
        })
      })
      .then(response => response.json())
      .then(result =>
      {
        // Print result
        content.value = result.traducao;
        click(content);
        //console.log(result.traducao);
      });
    });

  }
  let likes = document.querySelectorAll('.like');
  if(likes)
  {
    likes.forEach(like =>{
          like.style.animationPlayState = 'running';
          like.addEventListener('click', () =>
          {
              like.style.animationName = 'hide';
              like.style.animationPlayState = 'running';
              fetch("/likes", {method: 'POST',
              body: JSON.stringify
              ({
                  id: like.dataset.receita_id
              })
              })
              .then(responsejson => responsejson.json())
              .then(response=> {
                  like.addEventListener('animationend', function animation() {
                      like.removeEventListener('animationend', animation);
                      let liked = document.getElementById('like'+response.receita_id);
                      liked.classList.toggle("fa-solid");
                      liked.classList.toggle("fa-regular");
                      liked.style.animationName = 'show';
                      liked.style.animationDuration = '1s';
                      liked.style.animationPlayState = 'running';
                      setTimeout(() => {location.reload(true)}, 500);
                  });
              });
          });
      })
  }
  let cards_btn = document.querySelectorAll(".cards_btn");
  if(cards_btn)
  {
    cardbtn(cards_btn);
  }

});
function darkfull()
{
  document.querySelectorAll('.recipe-info').forEach(recipe_info=>
    {
      recipe_info.classList.toggle('textarea-dark')
    });
  document.querySelectorAll('.ingrdients-info').forEach(ingredientes_info=>
    {
      ingredientes_info.classList.toggle('textarea-dark')
    });
  document.querySelectorAll('.col-sm-2').forEach(col=>
    {
      col.classList.toggle('col-sm-2-black')
    });
}
