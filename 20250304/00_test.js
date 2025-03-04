// 실습 1번

// let radius = 5;
// const PI = 3.14;
// let area = PI * radius * radius;

// console.log(`반지름이 ${radius}인 원의 넓이는 ${area}입니다.`);


// 실습 2번

// let temparature = 25;

// if (temparature >= 30) {
//     console.log("집에 있자.");
// } else if (temparature >= 20) {
//     console.log("공원 가자.");
// } else if (temparature >= 10) {
//     console.log("카페 가자.");
// } else {
//     console.log("영화관 가자.");
// }


// 실습 3번

// let score = 40;

// if (score >= 60) {
//     console.log("합격입니다.");
// } else {
//     console.log("불합격입니다.");
// }


// 실습 4번

// let n1 = 1;
// let n2 = 100;
// let total = 0;

// for (let i = n1; i <= n2; i++) {
//     total += i;
// }

// console.log(`${n1}부터 ${n2}까지의 합은 ${total}입니다.`);


// 실습 5번

// let i = 1;

// while (true) {
//     if (i > 5) {
//         break;
//     }
//     console.log(i);
//     i++;
// }


// 실습 6번

let i = 0;

while (i <= 100) {
    i++;
    if (i % 3 !== 0) {
        continue;
    }
    console.log(i);
}
