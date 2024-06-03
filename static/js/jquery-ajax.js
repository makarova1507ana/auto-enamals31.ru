
// При нажатии на checkbox-кнопку отправляется get-запрос
$('input[checkbox-click]').on('click', function() {
    $(this).closest("form").submit();
});

// Функция для отображения сортировок на маленьком экране
$('#btn-filter').on('click', function() {
    document.getElementById("data-cards").style.display = "none";
    document.getElementById("paginator-block").style.display = "none";
    document.getElementById("filter-block").classList.remove('filter')
    document.getElementById("filter-block").classList.add('filter-full')
    document.getElementById("btn-cancel").style.display = "block";
});


// Функция для, для того чтобы вернуть все назад
$('#btn-cancel').on('click', function() {
    document.getElementById("data-cards").style.display = "block";
    document.getElementById("paginator-block").style.display = "block";
    document.getElementById("filter-block").classList.remove('filter-full')
    document.getElementById("filter-block").classList.add('filter')
    document.getElementById("btn-cancel").style.display = "none";
});



$('.required-delivery').click(function() {
    document.getElementById("id_delivery_address").required = true;
});


$(document).ready(function() {
    // Функция для отправки AJAX-запроса на сервер
    function updateCart(cartID, quantity, url) {
        console.log("Отправка AJAX-запроса для обновления корзины. ID корзины: ", cartID, " Количество: ", quantity);
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()  // CSRF-токен для безопасности
            },
            success: function(data) {
                console.log("Успешное обновление корзины. Новое количество: ", quantity);
                // Обновление значения в поле ввода на основе ответа сервера
                $('input[data-cart-id="' + cartID + '"]').val(quantity);
                 // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                //  var cartItemsContainer = $(`#product-${product_id}`);
                 console.log(data.cart_items_html)
                //  cartItemsContainer.html(data.cart_items_html);
                 location.reload()
            },
            error: function(data) {
                console.log('Ошибка при изменении количества');
            }
        });
    }

    // Обработчик для нажатия кнопок
    function handleButtonClick(event) {
        var $button = $(event.target);  // Кнопка, вызвавшая событие
        var $input = $button.siblings('input[data-count-product]');  // Поле ввода, связанное с кнопкой
        var value = parseInt($input.val());  // Текущее значение в поле ввода
        var max = $input.data('value');  // Максимальное значение
        var cartID = $input.data('cart-id');  // ID корзины
        var url = $input.data('cart-change-url');  // URL для изменения корзины

        // Обработка нажатия кнопки "увеличить"
        if ($button.hasClass('increment')) {
            console.log("Кнопка 'увеличить' нажата");
            if (value < max) {
                value += 1;
            }
        // Обработка нажатия кнопки "уменьшить"
        } else if ($button.hasClass('decrement')) {
            console.log("Кнопка 'уменьшить' нажата");
            if (value > 1) {
                value -= 1;
            }
        }

        // Обновление значения в поле ввода
        $input.val(value);
        // Отправка AJAX-запроса
        updateCart(cartID, value, url);
    }

    // Обработчик для изменения значения в input
    function handleInputChange(event) {
        var $input = $(event.target);  // Текущее поле ввода
        var value = parseInt($input.val());  // Значение в поле ввода
        var max = $input.data('value');  // Максимальное значение
        var cartID = $input.data('cart-id');  // ID корзины
        var url = $input.data('cart-change-url');  // URL для изменения корзины

        console.log("Изменение значения в input: ", value);

        // Проверка на валидность введенного значения
        if (isNaN(value) || value < 1) {
            value = 1;
        } else if (value > max) {
            value = max;
        }

        // Обновление значения в поле ввода
        $input.val(value);
        // Отправка AJAX-запроса
        updateCart(cartID, value, url);
    }

    // Привязка обработчиков к событиям
    $('.increment, .decrement').on('click', handleButtonClick);
    $('input[data-count-product]').on('focusout', handleInputChange);

    // Дополнительная проверка и логирование событий
    console.log("Скрипт инициализирован");
    $('.btn-increment').each(function() {
        console.log("Найдена кнопка 'увеличить': ", $(this));
    });
    $('.btn-decrement').each(function() {
        console.log("Найдена кнопка 'уменьшить': ", $(this));
    });
    $('input[data-count-product]').each(function() {
        console.log("Найдено поле ввода: ", $(this));
    });
});




// Выбор всех товаров
$('#select-all').on('change', function() {
    var url_value = $(this).data("cart-change-url");
    if( $(this).is(':checked') ) {
        select_all = 1
      } else {
        select_all = 0
      }

      console.log(url_value)

      const elements = document.querySelectorAll('.checkmark')
        var step;
        var s = []
        for (step = 0; step < elements.length; step++) {
          element =  elements[step];
          id_element = (element.value).toString()
    
            s.push(id_element)
        }
        carts_id = (s.join('.'));
        updateCart(carts_id, url_value,select_all)

        function updateCart(cart_id, url_value,select_all) {
            $.ajax({
                type: "GET",
                url: url_value,
                data: {
                    select_all:select_all,
                    cart_id: cart_id,
                },
                success: function (data){
                location.reload()
                },
                error: function (data) {
                    console.log("Ошибка при выборе всех элементов");
                },
            });
     }
});





// Когда html документ готов (прорисован)
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");

     // Ловим собыитие клика по кнопке добавить в корзину
     $(document).on("click", ".add-to-cart", function (e) {
         // Блокируем его базовое действие
         e.preventDefault();

         // Берем элемент счетчика в значке корзины и берем оттуда значение
         var goodsInCartCount = $("#goods-in-cart-count");
         var cartCount = parseInt(goodsInCartCount.text() || 0);
         var product_count = $(this).data("product-count");
         var product_cart = $(this).data("product-cart");

         if (product_cart >= product_count) {
            alert("Добавлено максимальное количества товара!");
            return;
         }


         // Получаем id товара из атрибута data-product-id
         var product_id = $(this).data("product-id");
         
         // Из атрибута href берем ссылку на контроллер django
         var add_to_cart_url = $(this).attr("href");

         // делаем post запрос через ajax не перезагружая страницу
         $.ajax({
             type: "POST",
             url: add_to_cart_url,
             data: {
                 product_id: product_id,
                 csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
             },
             success: function (data) {
                console.log('sss')
                 // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                 cartCount++;
                 goodsInCartCount.text(cartCount);

                 // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                 var cartItemsContainer = $(`#product-${product_id}`);
                 console.log(data.cart_items_html)
                 cartItemsContainer.html(data.cart_items_html);
             },

             error: function (data) {
                 console.log("Ошибка при добавлении товара в корзину");
             },
         });
     });


// Скрипт для добавления в корзину на странице детального отображения
 $(document).on("click", ".add-to-cart-detail", function (e) {
    // Блокируем его базовое действие
    e.preventDefault();

    // Берем элемент счетчика в значке корзины и берем оттуда значение
    var goodsInCartCount = $("#goods-in-cart-count");
    var cartCount = parseInt(goodsInCartCount.text() || 0);
    var product_count = $(this).data("product-count");
    var product_cart = $(this).data("product-cart");

    if (product_cart >= product_count) {
       alert("Добавлено максимальное количества товара!");
       return;
    }
    // Получаем id товара из атрибута data-product-id
    var product_id = $(this).data("product-id");

    // Из атрибута href берем ссылку на контроллер django
    var add_to_cart_url = $(this).attr("href");

    // делаем post запрос через ajax не перезагружая страницу
    $.ajax({
        type: "POST",
        url: add_to_cart_url,
        data: {
            product_id: product_id,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
            // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
            cartCount++;
            goodsInCartCount.text(cartCount);

            // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
            var cartItemsContainer = $('#cart');
            console.log(data.cart_items_html)
            cartItemsContainer.html(data.cart_items_html);
        },

        error: function (data) {
            console.log("Ошибка при добавлении товара в корзину");
        },
    });
});
    
    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".test", function (e) {
        // Блокируем его базовое действие
        e.preventDefault()

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var select_from_order = $(this).data("cart-change-url");
        // делаем post запрос через ajax не перезагружая страницу
        console.log(cart_id, select_from_order)
        $.ajax({
            type: "GET",
            url: select_from_order,
            data: {
                cart_id: cart_id,
            },
            success: function (data){
                var cartItemsContainer = $("#carts-container");
                 cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при удалении");
            },
        });
    });



    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault()
        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {



                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#carts-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при удалении");
            },
        });
    });


     // Теперь + - количества товара
     // Обработчик события для уменьшения значения


//    // Берем из разметки элемент по id - оповещения от django
//    var notification = $('#notification');
//    // И через 7 сек. убираем
//    if (notification.length > 0) {
//        setTimeout(function () {
//            notification.alert('close');
//        }, 500);
//    }

});

    //  $(document).on("click", ".decrement", function () {

    //     var product_q = $(this).data("value");
    //      // Берем ссылку на контроллер django из атрибута data-cart-change-url
    //      var url = $(this).data("cart-change-url");
    //      // Берем id корзины из атрибута data-cart-id
    //      var cartID = $(this).data("cart-id");
    //      // Ищем ближайшеий input с количеством
    //      var $input = $(this).closest('.center-block').find('.number');
    //      // Берем значение количества товара
    //      var currentValue = parseInt($input.val());
    //      // Если количества больше одного, то только тогда делаем -1

    //      if (currentValue > 1) {
    //          $input.val(currentValue - 1);
    //          // Запускаем функцию определенную ниже
    //          // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
    //          updateCart(cartID, currentValue - 1, -1, url);
    //      }

    //  });

    //  // Обработчик события для увеличения значения
    //  $(document).on("click", ".increment", function () {
    //      var product_q = $(this).data("value");
    //      // Берем ссылку на контроллер django из атрибута data-cart-change-url
    //      var url = $(this).data("cart-change-url");
    //      // Берем id корзины из атрибута data-cart-id
    //      var cartID = $(this).data("cart-id");
    //      // Ищем ближайшеий input с количеством
    //      var $input = $(this).closest('.center-block').find('.number');

    //      // Берем значение количества товара
    //      var currentValue = parseInt($input.val());

    //     if (currentValue >= product_q) {
    //          $input.val(product_q);
    //          }
    //     else{
    //         $input.val(currentValue + 1);
    //     }



    //      // Запускаем функцию определенную ниже

    //      // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
    //      updateCart(cartID, currentValue + 1 , 1, url);
    //  });

    //  function updateCart(cartID, quantity, change, url) {
    //      $.ajax({
    //          type: "POST",
    //          url: url,
    //          data: {
    //              cart_id: cartID,
    //              quantity: quantity,
    //              csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    //          },

    //          success: function (data) {
    //               // Сообщение

    //              // Изменяем количество товаров в корзине
    //              var goodsInCartCount = $("#goods-in-cart-count");
    //              var cartCount = parseInt(goodsInCartCount.text() || 0);
    //              cartCount += change;
    //              goodsInCartCount.text(cartCount);

    //              // Меняем содержимое корзин
    //               var cartItemsContainer = $("#carts-container");
    //              cartItemsContainer.html(data.cart_items_html);

    //          },
    //          error: function (data) {
    //              console.log("Ошибка при добавлении товара в корзину");
    //          },
    //      });
    //  }




