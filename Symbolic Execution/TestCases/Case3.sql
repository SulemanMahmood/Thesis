Truncate Table numbers;
insert into numbers(num1, num2, num3) values (4, 8, 1);
insert into numbers(num1, num2, num3) values (5, 1, 0);
commit;
Select ReadNum2(0);
