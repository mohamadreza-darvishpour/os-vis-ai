
let last_prod_num = 0 ; 
let last_prod_name = 'last_prod_name_in_js';
function loadMoreProducts(){

    $.ajax({
        url: '.' , 
        method : 'POST' , 
        headers : {
                'X-CSRFToken' : $('#csrf_token').val()
                 },
        data : {
          
        },

        success : function(response){
            console.log(response);
            response.products.forEach(function(product){
                const productHtml = `
                
                <div class="col-md-6 col-lg-6 col-xl-4">
                <div class="rounded position-relative fruite-item">
                    <div class="fruite-img">
                        <img src="/static/img/fruite-item-5.jpg" class="img-fluid w-100 rounded-top" alt="">
                    </div>
                    <div class="text-white bg-secondary px-3 py-1 rounded position-absolute" style="top: 10px; left: 10px;">${product.tag}</div>
                    <div class="p-4 border border-secondary border-top-0 rounded-bottom">
                        <h4>${product.name}</h4>
                        <p>${product.description}</p>
                        <div class="d-flex justify-content-between flex-lg-wrap">
                            <p class="text-dark fs-5 fw-bold mb-0"> ${product.price} $ </p>
                            <a href="#" class="btn border border-secondary rounded-pill px-3 text-primary"><i class="fa fa-shopping-bag me-2 text-primary"></i> Add to cart</a>
                        </div>
                    </div>
                </div>
            </div>
                `;
                $(`#product_list_div99`).append(productHtml);
             
            })
            if(response.products.length < 1 ){
                window.alert('products_ended')
            };
            last_prod_num ++ ; 
        },
        
        
        error : function(){
            alert("error loading more products");
            alert($('#csrf_token').val());
        }

    });
};

$('#load_more_btn').on('click' , function(){
    loadMoreProducts();

});






