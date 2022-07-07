'use strict';

window.addEventListener('DOMContentLoaded', () => { 

    const screenWidth = screen.width;

    let wheelSet = {
        wrapWidth: 850,
        outerRadius: 420,
        textFontSize: 24,
        lineWidth: 3
    };

    // if (screenWidth < 1200) {
    //     wheelSet.outerRadius = 360;
    //     wheelSet.textFontSize = 16;
    //     wheelSet.wrapWidth = 620;
    // }

    // console.log(document.getElementById('canvas'));

    let theWheel = new Winwheel({
        'outerRadius'     : wheelSet.outerRadius,       
        'textFontSize'    : wheelSet.textFontSize,        
        'textOrientation' : 'horizontal', 
        'textAlignment'   : 'center',    
        'numSegments'     : 10,
        'lineWidth'   : wheelSet.lineWidth,    
        'strokeStyle' :  '#8BA93B',
        'textFontWeight' : 'normal',
        'textFillStyle': '#111505',
        'segments'        :      
        [
            {'fillStyle' : '#fff', 'text' : `
            Руководство
            «Оберег от клещей»
           `},
           {'fillStyle' : '#C4E46D', 'text' :  `         Барберин`},
           {'fillStyle' : '#fff', 'text' : `
            Руководство 
            «Антигистаминовый 
            протокол питания»
            `},
           {'fillStyle' : '#C4E46D', 'text' : `
            Набор антибиотик 
            ФИТОТОТАЛ
            `},
           {'fillStyle' : '#fff', 'text' : `
           Руководство 
           «Оберег от клещей» 
           `},
           {'fillStyle' : '#C4E46D', 'text' : `
            50% скидка 
            на все руковдства
            `},
           {'fillStyle' : '#fff', 'text' : `
            50% скидка 
            на все руковдства
            `},
           {'fillStyle' : '#C4E46D', 'text' : `
            Руководство 
            «Антигистаминовый
             протокол питания» 
            `},
           {'fillStyle' : '#fff', 'text' : `
            Набор грибной 
           антипаразитарный
           `},
           {'fillStyle' : '#C4E46D', 'text' : `
            Антипаразитарный
            комлекс от ВИТАУКТ
           `}
        ],
        'animation' :           // Specify the animation to use.
        {
            'type'     : 'spinToStop',
            'duration' : 5,
            'spins' : 3,
            'callbackFinished': clearWheel,
            // 'repeat' : 2
        }
    });

    function clearWheel() {
        theWheel.rotationAngle = 0;
    }


    const wheelButton = document.querySelector('.wheel__button');

    const spanCount = document.querySelector('.spins span');

    let spinsAvalible = spanCount.textContent;

    let canSpin = true;
    const spinButton = document.querySelector('.wheel__button button');

    const prizeWrap = document.querySelector('.prize__info');
    const prizeSpan = document.querySelector('.prize__info span');

    if (spanCount.textContent == 0) {
        spinButton.classList.add('disabled');
    }

    wheelButton.addEventListener('click', (e) => {
        e.preventDefault();

        if (canSpin) {
            fetch(`get_reward/${email}/?key=${key}`)
            .then((response) => {
//                console.log(response);
                return response.json();
            })
            .then((data) => {
                    console.log(data);
                    if (data.success) {
                        canSpin = false;
                        spanCount.innerHTML = spanCount.textContent - 1;
                        spinButton.classList.add('disabled');
                        setTimeout(() => {
                            if (spanCount.textContent > 0) {
                                canSpin = true;
                                spinButton.classList.remove('disabled');
                            }
                        }, 5100);
                        setTimeout(() => {
                            prizeSpan.innerHTML = data.reward_text;
                            prizeWrap.classList.add('active');
                            setTimeout(() => {
                                prizeWrap.classList.remove('active');
                            }, 3000);
                        }, 5000);

                        theWheel.draw();
                        let stopAt = theWheel.getRandomForSegment(data.reward_code + 1);
                        theWheel.animation.stopAngle = stopAt;
                        theWheel.startAnimation();

                        if (spanCount.textContent == 0) {
                            spinButton.classList.add('disabled');
                        }
                    } else {
                        spinButton.classList.add('disabled');
                    }
            })
            .catch((e) => {
                console.log(e)
            });
        }
    })
});