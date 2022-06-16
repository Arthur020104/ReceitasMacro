import {alert} from './script.js'
export function click(content)
{
    let foods = content.value.split('\n');
    for(let food=0; food< foods.length;food++){foods[food] = foods[food].trim()}
    let nutricion = {"calorias": 0, "carboidratos":0, "proteinas": 0, "gorduras":0};
    let counter = 0;
    alert({"loading":"Carregando..."})
    for(let food=0; food< foods.length;food++)
    {
    fetch(`https://api.edamam.com/api/nutrition-data?app_id=0e0efa68&app_key=%206106f458ccc594574d31692d70661790%09&nutrition-type=cooking&ingr=${foods[food]}`)
    .then(resp => resp.json())
    .then(resp =>
    {
        if(resp)
        {
        try
        {
            nutricion.calorias += resp.calories;
            nutricion.carboidratos += resp['totalNutrients'].CHOCDF.quantity;
            nutricion.proteinas += resp['totalNutrients'].PROCNT.quantity;
            nutricion.gorduras +=  resp['totalNutrients'].FAT.quantity;
            counter++;
            if(foods.length == food+1)
            {
                document.getElementById("nutricion").value = nutricion.calorias+","+nutricion.carboidratos+","+nutricion.proteinas+","+ nutricion.gorduras;
            }
        }
        catch(e)
        {
            counter--;
            console.log(e);
            if(e instanceof TypeError)
            {
            let comida;
            fetch('/tradutor',
            {
                method : 'POST',
                body: JSON.stringify(
                {
                traduzir: foods[food],
                lang: "pt"
                })
            })
            .then(response => response.json())
            .then(result =>
            {
                console.log(result.traducao);
                comida = result.traducao;
            });
            setTimeout(() => {alert({"error":"TypeError:Por favor especificar melhor a quantidade do alimento "+comida+"."});}, 300);
            }
            else
            {
            alert({"error":e});
            }
        }
        }
    });

    }
    return document.getElementById("recipe-make").disabled = false;

}