# Pinky语言编译器

学习课程[Pikuma](https://pikuma.com/courses/create-a-programming-language-compiler)写的Pinky编译器。

## Pinky语言语法

Pinky语言的语法介绍可以通过以下链接访问：[Pinky语言语法](https://pinky-lang.org/)。
支持以下控制结构：

- **条件语句**：`if`，`else`
- **循环结构**：`for`，`while`
- **函数定义**：支持函数的创建与调用

## 执行方式

支持三种执行方式：

1. **解释器**：
   - 直接遍历抽象语法树（AST）进行执行。

2. **虚拟机 (VM)**：
   - 编译为字节码，由栈式虚拟机执行。

3. **LLVM**：
   - 生成与Pinky对应的LLVM IR,编译为机器码，在CPU上执行。
  
## 优化
   - 支持AST常量折叠。

## 可视化网站

可以访问以下可视化网站，体验Pinky语言的各种功能和执行效果：
- [Pinky可视化网站](http://39.107.107.227:5000/)
