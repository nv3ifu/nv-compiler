; ModuleID = "nv_module"
target triple = "x86_64-w64-windows-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"pow"(double %".1", double %".2")

define i32 @"main"()
{
entry:
  %".2" = getelementptr inbounds [3 x i8], [3 x i8]* @".str.0", i32 0, i32 0
  %".3" = getelementptr inbounds [4 x i8], [4 x i8]* @".str.1", i32 0, i32 0
  %".4" = getelementptr inbounds [3 x i8], [3 x i8]* @".str.2", i32 0, i32 0
  %".5" = getelementptr inbounds [4 x i8], [4 x i8]* @".str.3", i32 0, i32 0
  %".6" = getelementptr inbounds [3 x i8], [3 x i8]* @".str.4", i32 0, i32 0
  %".7" = getelementptr inbounds [4 x i8], [4 x i8]* @".str.5", i32 0, i32 0
  %".8" = getelementptr inbounds [18 x i8], [18 x i8]* @".str.6", i32 0, i32 0
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".8")
  %"i" = alloca double
  store double 0x3ff0000000000000, double* %"i"
  br label %"for.cond"
for.cond:
  %"i.val" = load double, double* %"i"
  %"for.cmp" = fcmp olt double %"i.val", 0x4014000000000000
  br i1 %"for.cmp", label %"for.body", label %"for.end"
for.body:
  %"i.val.1" = load double, double* %"i"
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".3", double %"i.val.1")
  br label %"for.step"
for.step:
  %"i.val.2" = load double, double* %"i"
  %"for.next" = fadd double %"i.val.2", 0x3ff0000000000000
  store double %"for.next", double* %"i"
  br label %"for.cond"
for.end:
  %".17" = getelementptr inbounds [25 x i8], [25 x i8]* @".str.7", i32 0, i32 0
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".17")
  %"j" = alloca double
  store double              0x0, double* %"j"
  br label %"for.cond.1"
for.cond.1:
  %"j.val" = load double, double* %"j"
  %"for.cmp.1" = fcmp olt double %"j.val", 0x4024000000000000
  br i1 %"for.cmp.1", label %"for.body.1", label %"for.end.1"
for.body.1:
  %"j.val.1" = load double, double* %"j"
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".3", double %"j.val.1")
  br label %"for.step.1"
for.step.1:
  %"j.val.2" = load double, double* %"j"
  %"for.next.1" = fadd double %"j.val.2", 0x4000000000000000
  store double %"for.next.1", double* %"j"
  br label %"for.cond.1"
for.end.1:
  %".26" = getelementptr inbounds [20 x i8], [20 x i8]* @".str.8", i32 0, i32 0
  %".27" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".26")
  %"mul" = fmul double 0x4014000000000000, 0x4000000000000000
  %"add" = fadd double 0x4024000000000000, %"mul"
  %"x" = alloca double
  store double %"add", double* %"x"
  %"x.val" = load double, double* %"x"
  %".29" = call i32 (i8*, ...) @"printf"(i8* %".3", double %"x.val")
  %".30" = getelementptr inbounds [12 x i8], [12 x i8]* @".str.9", i32 0, i32 0
  %".31" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".30")
  %"x.val.1" = load double, double* %"x"
  %"gt" = fcmp ogt double %"x.val.1", 0x402e000000000000
  br i1 %"gt", label %"if.then", label %"if.else"
if.then:
  %".33" = getelementptr inbounds [13 x i8], [13 x i8]* @".str.10", i32 0, i32 0
  %".34" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".33")
  br label %"if.end"
if.else:
  %".36" = getelementptr inbounds [14 x i8], [14 x i8]* @".str.11", i32 0, i32 0
  %".37" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".36")
  br label %"if.end"
if.end:
  %".39" = getelementptr inbounds [15 x i8], [15 x i8]* @".str.12", i32 0, i32 0
  %".40" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".39")
  %"n" = alloca double
  store double 0x4008000000000000, double* %"n"
  br label %"while.cond"
while.cond:
  %"n.val" = load double, double* %"n"
  %"gt.1" = fcmp ogt double %"n.val",              0x0
  br i1 %"gt.1", label %"while.body", label %"while.end"
while.body:
  %"n.val.1" = load double, double* %"n"
  %".44" = call i32 (i8*, ...) @"printf"(i8* %".3", double %"n.val.1")
  %"n.val.2" = load double, double* %"n"
  %"sub" = fsub double %"n.val.2", 0x3ff0000000000000
  store double %"sub", double* %"n"
  br label %"while.cond"
while.end:
  %".47" = getelementptr inbounds [18 x i8], [18 x i8]* @".str.13", i32 0, i32 0
  %".48" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".47")
  %"call.add" = call double @"add"(double 0x4008000000000000, double 0x4010000000000000)
  %"result" = alloca double
  store double %"call.add", double* %"result"
  %"result.val" = load double, double* %"result"
  %".50" = call i32 (i8*, ...) @"printf"(i8* %".3", double %"result.val")
  %".51" = getelementptr inbounds [6 x i8], [6 x i8]* @".str.14", i32 0, i32 0
  %".52" = call i32 (i8*, ...) @"printf"(i8* %".5", i8* %".51")
  ret i32 0
}

@".str.0" = private constant [3 x i8] c"%g\00"
@".str.1" = private constant [4 x i8] c"%g\0a\00"
@".str.2" = private constant [3 x i8] c"%s\00"
@".str.3" = private constant [4 x i8] c"%s\0a\00"
@".str.4" = private constant [3 x i8] c"%d\00"
@".str.5" = private constant [4 x i8] c"%d\0a\00"
define double @"add"(double %"a", double %"b")
{
entry:
  %"a.1" = alloca double
  store double %"a", double* %"a.1"
  %"b.1" = alloca double
  store double %"b", double* %"b.1"
  %"a.val" = load double, double* %"a.1"
  %"b.val" = load double, double* %"b.1"
  %"add" = fadd double %"a.val", %"b.val"
  ret double %"add"
}

@".str.6" = private constant [18 x i8] c"Testing for loop:\00"
@".str.7" = private constant [25 x i8] c"Testing for with step 2:\00"
@".str.8" = private constant [20 x i8] c"Testing arithmetic:\00"
@".str.9" = private constant [12 x i8] c"Testing if:\00"
@".str.10" = private constant [13 x i8] c"x > 15: true\00"
@".str.11" = private constant [14 x i8] c"x > 15: false\00"
@".str.12" = private constant [15 x i8] c"Testing while:\00"
@".str.13" = private constant [18 x i8] c"Testing function:\00"
@".str.14" = private constant [6 x i8] c"Done!\00"