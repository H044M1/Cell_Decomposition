Декомпозиция на клетки (Cell decomposition)
Задача Дана двумерная плоскость, на которой находятся объекты-препятствия. По плоскости движется робот - материальная точка с координатой (Cx, Cy); робот может перемещаться в любом направлении без ограничений. 
Заданы начальная и конечная координаты робота Init=(Initx, Inity) и Goal=(Goalx, Goaly). Требуется: найти кратчайший, по возможности, путь для робота из начальной координаты в конечную, 
не приводящий к столкновению робота с препятствиями, или определить, что такого пути не существует. 
 
 Вид препятствий - круг, который задаётся координатой центра и радиусом.
 
 ![image](https://github.com/H044M1/Cell_Decomposition/assets/116296089/9b1371b6-254c-4225-aec4-70b3f38489e9)

Клетки делятся на две группы - свободные и занятые, свободные клетки полностью лежат в Cfree, занятые - частично или полностью пересекаются с Cobs (в этом смысле разбиение является приблизительным - approximate cell decomposition). 
Разбиение может проводиться разными способами - рекурсивно (допускаются клетки разного размера; занятые клетки, частично пересекающиеся с Cobs, разбиваются дальше до некоторого минимального предела) или регулярно (все клетки одного размера).

![image](https://github.com/H044M1/Cell_Decomposition/assets/116296089/f88e6835-b27a-4864-9a3c-fe6e5549720d)

Вводится граф, где вершинами являются свободные клетки. Соседние свободные клетки, допускающие переход из одной клетки в другую, связываются ребром; это клетки, или имеющие общую сторону (движение по горизонтали и вертикали),
или общую вершину (движение по диагонали - возможно в случае, если при переходе не происходит столкновения с занятыми клетками). 
Вес ребра - длина пути (перехода) из одной клетки в другую; можно считать, что робот движется между центрами клеток. 
Для полученного графа решается задача поиска кратчайшего пути, затем по найденному решению строится итоговый маршрут.

![image](https://github.com/H044M1/Cell_Decomposition/assets/116296089/868bfafe-7d4f-4fe1-b206-aaa77f067693)
![image](https://github.com/H044M1/Cell_Decomposition/assets/116296089/9e32c4e9-80a8-4838-87cc-fce65ff56d4d)

GUI написан на PyQt5, есть возможность загружать и выгружать сцены Результаты работы программы:
![image](https://github.com/H044M1/Cell_Decomposition/assets/116296089/907039c1-0fe2-4eb4-98fd-b053e8ba805a)
![image](https://github.com/H044M1/Cell_Decomposition/assets/116296089/49c77a46-d7b3-4487-b149-b966a2d1a3ca)

