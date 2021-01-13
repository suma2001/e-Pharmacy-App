jQuery(document).ready(function($){

    $('.img1').on({
         'click': function(){
             $('#change-image').attr('src','https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQ51vSDuotgp6UsSw7G-nzuBewVmpctHvS8mPEsLajFNZ_hoiWf');
         }
     });
     
    $('.img2').on({
         'click': function(){
             $('#change-image').attr('src','https://www.buy-pharma.md/img/uploads/42678-Absolut-3G-Box-And-Capsules.jpg');
         }
     });
     
    $('.img3').on({
         'click': function(){
             $('#change-image').attr('src','https://images-na.ssl-images-amazon.com/images/I/7125T4RvGSL._SX679_.jpg');
         }
     });
    });