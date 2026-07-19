# ===== RELEASE pytorch/pytorch v1.9.0 =====

# **PyTorch 1.9 Release Notes** 

* Highlights
* Backwards Incompatible Change
* Deprecations
* New Features
* Improvements
* Bug Fixes
* Performance
* Documentation

# Highlights

We are excited to announce the release of PyTorch 1.9. The release is composed of more than 3,400 commits since 1.8, made by 398 contributors. Highlights include:

* Major improvements to support scientific computing, including torch.linalg, torch.special, and Complex Autograd
* Major improvements in on-device binary size with Mobile Interpreter
* Native support for elastic-fault tolerance training through the upstreaming of TorchElastic into PyTorch Core
* Major updates to the PyTorch RPC framework to support large scale distributed training with GPU support
* New APIs to optimize performance and packaging for model inference deployment 
* Support for Distributed training, GPU utilization and SM efficiency in the PyTorch Profiler

We’d like to thank the community for their support and work on this latest release. We’d especially like to thank Quansight and Microsoft for their contributions.

You can find more details on all the highlighted features in the [_PyTorch 1.9 Release blogpost_](https://pytorch.org/blog/pytorch-1.9-released/). 

# Backwards Incompatible changes

## Python API

* **`torch.divide` with `rounding_mode='floor'` now returns infinity when a non-zero number is divided by zero (**[**#56893**](https://github.com/pytorch/pytorch/pull/56893)**).**
This fixes the `rounding_mode='floor'` behavior to return the same non-finite values as other rounding modes when there is a division by zero. Previously it would always result in a NaN value, but a non-zero number divided by zero should return +/- infinity in IEEE floating point arithmetic. Note this does not effect `torch.floor_divide` or the floor division operator, which currently use `rounding_mode='trunc'` (and are also deprecated for that reason).

<p align="center">
  <table align="center">
    <tr><th>1.8.1</th><th>1.9.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> a = torch.tensor([-1.0, 0.0, 1.0])
>>> b = torch.tensor([0.0])
>>> torch.divide(a, b, rounding_mode='floor')
tensor([nan, nan, nan])
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> a = torch.tensor([-1.0, 0.0, 1.0])
>>> b = torch.tensor([0.0])
>>> torch.divide(a, b, rounding_mode='floor')
tensor([-inf, nan, inf])
      </pre></sub></td>
    </tr>
  </table>
</p>
        

* **Legacy tensor constructors and `Tensor.new` no longer support passing both `Tensor` and `device` as inputs  ([#58108](https://github.com/pytorch/pytorch/pull/58108)).**
This fixes a bug in which 1-element integer tensors were misinterpreted as specifying tensor size, yielding an uninitialized tensor. As noted in the error message, use the new-style `torch.tensor(...)` or `torch.as_tensor(...)` to copy or alias an existing tensor. If you want to create an uninitialized tensor, use `torch.empty(...)`. 
<p align="center">
  <table align="center">
    <tr><th>1.8.1</th><th>1.9.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> a = torch.tensor([1])
>>> torch.LongTensor(a, device='cpu') # uninitialized
tensor([7022349217739848992])
>>> a.new(a, device='cpu')
tensor([4294967295]) # uninitialized
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> a = torch.tensor([1])
>>> torch.LongTensor(a, device='cpu')
RuntimeError: Legacy tensor constructor of the form torch.Tensor(tensor, device=device) is
not supported. Use torch.tensor(...) or torch.as_tensor(...) instead.
>>> a.new(a, device='cpu')
RuntimeError: Legacy tensor new of the form tensor.new(tensor, device=device) is not
supported. Use torch.as_tensor(...) instead.
      </pre></sub></td>
    </tr>
  </table>
</p>        
        
* **`torch.divide` with `rounding_mode='true'` is replaced with `rounding_mode=None` ([#51988](https://github.com/pytorch/pytorch/pull/51988)).**
`torch.divide`'s undocumented `rounding_mode='true'` option has been removed, and instead `rounding_mode=None` should be passed to indicate no rounding should take place. This is equivalent to omitting the argument entirely.

<p align="center">
  <table align="center">
    <tr><th>1.8.1</th><th>1.9.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> a, b = torch.full((2,), 4.2), torch.full((2,), 2)
>>> torch.divide(a, b, rounding_mode='true')
tensor([2.1000, 2.1000])
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> a, b = torch.full((2,), 4.2), torch.full((2,), 2)
>>> torch.divide(a, b, rounding_mode=None) # equivalent to  torch.divide(a, b, rounding_mode='true') from the prior release
tensor([2.1000, 2.1000])
      </pre></sub></td>
    </tr>
  </table>
</p>

* **`import torch.tensor as tensor` is no longer supported ([#53424](https://github.com/pytorch/pytorch/pull/53424)).**
Instead, use `from torch import tensor`

<p align="center">
  <table align="center">
    <tr><th>1.8.1</th><th>1.9.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> import torch.tensor as tensor
>>> torch.tensor(1.)
tensor(1.)
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> import torch.tensor as tensor
ModuleNotFoundError: No module named 'torch.tensor'
>>> from torch import tensor
>>> tensor(1.)
tensor(1.)
      </pre></sub></td>
    </tr>
  </table>
</p>

* **binary release: `numpy` is no longer a required dependency**
If you require `numpy` (and don't already have it installed) you will need to install it separately.


## Autograd

* **`torch.autograd.gradcheck.get_numerical_jacobian` and `torch.autograd.gradcheck.get_analytical_jacobian` no longer support functions that return complex valued output as well as any other values of `grad_out` not equal to 1** ([#55692](https://github.com/pytorch/pytorch/pull/55692)).
This change is a part of a refactor of `gradcheck`’s internals. Note that `gradcheck` itself still supports functions with complex output. This new restriction only applies to calls to the two internal helper functions. As a workaround, you can wrap your functions to return either the real or imaginary component of its output before calling these functions. Additionally these internal helpers no longer accept any other value except 1 for `grad_out` for any input function. Note that these helper functions are also being deprecated in this release.
 
1.8.1:
```python
get_numerical_jacobian(torch.complex, (a, b), grad_out=2.0)
```

1.9.0:
```python
      def wrapped(fn):
            def wrapper(*input):
                return torch.real(fn(*input))
            return wrapper
        
        get_numerical_jacobian(wrapped(torch.complex), (a, b), grad_out=1.0)
```

* **`torch.autograd.gradcheck` now throws `GradcheckError`** ([#55656](https://github.com/pytorch/pytorch/pull/55656)).
This change is a part of a refactor of `gradcheck`’s internals. All errors that are able to be silenced by `raise_exception=False` now raise `GradcheckError` (which inherits from `RuntimeError`). If you explicitly check that the type of the error is `RuntimeError` you'll need to update your code to check for `GradcheckError` instead. Otherwise if you use something like `except` or `isinstance`, no changes are necessary.

1.8.1:
```python
# An example of a situation that will now return GradcheckError instead of
# RuntimeError is when there is a jacobian mismatch, which can happen
# for example when you forget to specify float64 for your inputs.
try:
    torch.autograd.gradcheck(torch.sin, (torch.ones(1, requires_grad=True),))
except RuntimeError as e:
    assert type(e) is RuntimeError # explicitly check type -> NEEDS UPDATE
```

1.9.0:
```python
try:
    torch.autograd.gradcheck(torch.sin, (torch.ones(1, requires_grad=True),)
except RuntimeError as e:
   # GradcheckError inherits from RuntimeError so you can still catch this
   # with RuntimeError (No change necessary!)
   
   # BUT, if you explicitly check type...
   assert type(e) is torch.autograd.GradcheckError
```

* **Finished deprecation cycle for in-place view error checks** ([#56093](https://github.com/pytorch/pytorch/pull/56093)).
 In-place modification of views will now raise an error if that view was created by a custom function or a function that returns multiple views, or if the view was created in no-grad mode. Modifying in-place a view created in the situations above are error-prone and have been deprecated since v1.5.0. Doing these in-place modifications are now forbidden. For more information on how to work around this, see the related sections the release notes linked below:
    * [v1.5.0](https://github.com/pytorch/pytorch/releases?after=v1.5.1) (view created in custom autograd function, view created in no-grad block)
    * [v1.7.0](https://github.com/pytorch/pytorch/releases?after=v1.8.0-rc3) (section on `split` and `chunk`, i.e., functions that return multiple views).

## torch.nn

* **Fixed regression for `nn.MultiheadAttention` to now apply bias flag to both in and out projection layers** ([#52537](https://github.com/pytorch/pytorch/pull/52537)).
In PyTorch 1.6, a regression was introduced that caused the `bias` flag of `nn.MultiheadAttention` only to apply to the input projection layer. This caused the output projection layer to always include a `bias` parameter, even with `bias=False` specified. The regression is now fixed in PyTorch 1.9, making the `bias` flag correctly apply to both the input and output projection layers. This fix is BC-breaking for the `bias=False` case as it will now result in no `bias` parameter for the output projection layer.

<p align="center">
  <table align="center">
    <tr><th>v1.6 - v1.8.1:</th><th>pre 1.6 & 1.9.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> mha = torch.nn.MultiheadAttention(4, 2, bias=False)
>>> print(mha.out_proj.bias)
Parameter containing:
tensor([0., 0., 0., 0.], requires_grad=True)
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> mha = torch.nn.MultiheadAttention(4, 2, bias=False)
>>> print(mha.out_proj.bias)
None
      </pre></sub></td>
    </tr>
  </table>
</p>


* **Updated `nn.Module` to fire full backward hooks even when no input requires grad** ([#56693](https://github.com/pytorch/pytorch/pull/56693)).
Prior to this release, full backward hooks were not fired when no input requires gradients. This has been changed so that full backward hooks will always fire during the backward pass, regardless of whether or not any input requires gradients. If you are using full backward hooks, be aware that they may fire more frequently than pre-1.9 due to this change.

<p align="center">
  <table align="center">
    <tr><th>1.8.1:</th><th>1.9.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> m = torch.nn.Linear(2, 3)
>>> def hook(mod, grad_input, grad_output):
>>> print('hook called:', grad_input, grad_output)
>>> m.register_full_backward_hook(hook)
>>> input_no_grad = torch.rand(1, 2, requires_grad=False)
>>> m(input_no_grad).sum().backward()
>>> input_grad = torch.rand(1, 2, requires_grad=True)
>>> m(input_grad).sum().backward()
hook called: (tensor([[0.1478, 0.6517]]),) (tensor([[1., 1., 1.]]),)
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> m = torch.nn.Linear(2, 3)
>>> def hook(mod, grad_input, grad_output):
>>> print('hook called:', grad_input, grad_output)
>>> m.register_full_backward_hook(hook)
>>> input_no_grad = torch.rand(1, 2, requires_grad=False)
>>> m(input_no_grad).sum().backward()
hook called: (None,) (tensor([[1., 1., 1.]]),)
>>> input_grad = torch.rand(1, 2, requires_grad=True)
>>> m(input_grad).sum().backward()
hook called: (tensor([[0.1478, 0.6517]]),) (tensor([[1., 1., 1.]]),)
      </pre></sub></td>
    </tr>
  </table>
</p>

## Dataloader

* **Add Numpy seeding to worker of DataLoader** ([#56488](https://github.com/pytorch/pytorch/pull/56488)).
`DataLoader` with `num_workers > 0` will now set independent random seed for NumPy random functions on each worker by default. So, users now won’t be required to set random seed for NumPy using `worker_init_fn` to force NumPy random operations deterministic and independent across `DataLoader` workers. This PR won’t affect users who have already set random seed for NumPy random functions using `worker_init_fn`.
```python 
        # dataset returns numpy.random.randint(1, 10000) 
        ctx = mp.get_context('fork')
        gen = torch.Generator().manual_seed(0)
        dl = DataLoader(dataset, batch_size=2, num_workers=2, multiprocessing_context=ctx, generator=gen)
        for epoch in range(2):
            print("=" * 4, "Epoch", epoch, "=" * 4)
            for batch in dl:
                print(batch)
```
        
<p align="center">
  <table align="center">
    <tr><th>1.8.1:</th><th>1.9.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
# When using fork, each worker has same random seed for NumPy random functions at each epoch.
========== Epoch 0 ==========
tensor([[ 0, 340],
[ 1, 7512]])
tensor([[ 2, 340],
[ 3, 7512]])
========== Epoch 1 ==========
tensor([[ 0, 340],
[ 1, 7512]])
tensor([[ 2, 340],
[ 3, 7512]])
      </pre></sub></td>
      <td><sub><pre lang="python">
# Random seeds for NumPy are different across `DataLoader` workers in each epoch.
========== Epoch 0 ==========
tensor([[ 0, 8715],
[ 1, 5555]])
tensor([[ 2, 6379],
[ 3, 1432]])
========== Epoch 1 ==========
tensor([[ 0, 1374],
[ 1, 996]])
tensor([[ 2, 143],
[ 3, 3507]])
      </pre></sub></td>
    </tr>
  </table>
</p>


* **Added static type checking enforce for DataPipe** ([#54020](https://github.com/pytorch/pytorch/pull/54020)).

A new attribute named `type` has been introduced for `IterableDataset` using the typing annotation at each class declaration. By adding this attribute, we are able to extend `IterableDataset` to have type inference and lazy initialization to incorporate the new DataLoader architecture. But, several BC-breaking restrictions are introduced due to this feature.

1.8.1:
```python
# Users can use string to bypass the invalid type annotation without any error. 
# And, incorrect type annotations attached to `__iter__` function are ignored.
```

1.9.0:
```python
# The following scenario will now raise different Exceptions
# 1) The type annotation is required to be valid now. Previous workaround
# like using string to  represent the invalid type annotation is not supported now.

# Raises Exception from the evaluation `eval("invalid_type", globals, locals)`
class DS(IterableDataset["invalid_type"]):  
     ...
# Raises TypeError if the return type of __iter__ is not an Iterator
class DS(IterableDataset[str]):
    def __iter__(self) -> str:
      ...
# Raise TypeError if the return type of __iter__ is of the form Iterator[X], 
# but the argument type X is not a subtype of the IterableDataset.type attribute.
class DS(IterableDataset[str]):
    def __iter__(self) -> Iterator[int]:
       ...

#  IterableDatset now has a metaclass, which will conflict with
#  existing user-defined metaclasses on IterableDatasets
class DS(IterableDataset[str], metaclass=MyMeta): 
    ...
```


## Meta API

* **Given Tensor a non-trivial (for now) metaclass _TensorMeta** ([#56147](https://github.com/pytorch/pytorch/pull/56147)).
Tensor now has a non-trivial metaclass. This shouldn't be user observable, as Tensor already inherits from a C defined class (and is thus incompatible with other typical metaclasses), but there may be unanticipated interactions with other language features in Python. This PR changes the metaclass of torch.tensor. I.e. `type(type(torch.tensor([1])))` now prints `<class 'torch._C._TensorMeta'>` (used to be `<class 'type'>`)

## C++ API

* **Changed in-place resize functions to return const Tensor&** ([#55351](https://github.com/pytorch/pytorch/pull/55351)).
The C++ signature for `resize_`, `resize_as_`, `resize_as_sparse_`, `sparse_resize_`, and `sparse_resize_and_clear_` has changed to return a `const Tensor&` instead of a `Tensor&`. This may break users’ TORCH_LIBRARY operators that called these functions but returned a non-const `Tensor&`. Ideally, users can change their operators to also consume and return `const Tensor&`, but simply casting the result of the changed function with `const_cast<Tensor&>` is also an option.

1.8.1:
```cpp
const at::Tensor a = at::randn({2, 2});
const at::Tensor b = at::ones({1, 4}, at::kInt);
at::Tensor& out = at::resize_as_(a, b); # success
```

1.9.0:
```cpp
const at::Tensor b = at::ones({1, 4}, at::kInt);
at::Tensor& out = at::resize_as_(a, b); 
# error: binding value of type 'const at::Tensor' to reference to type 'at::Tensor' drops 'const' qualifier
const at::Tensor& out = at::resize_as_(a, b); # Success
```

* **Some ATen Reduction Ops as well as `kron_out` now throw an error when an undefined tensor is passed as input for `out` argument** ([#53218](https://github.com/pytorch/pytorch/pull/53218), [#53640](https://github.com/pytorch/pytorch/pull/53640)).
    * C++ API for the reductions ops like `sum_out`, `nansum_out`, `prod_out`, `std_var_out` have been changed to require users allocating result Tensor before calling these ops. The C++ API `allocate_reduction_result` has changed to `resize_reduction_result` to disallow allocating result Tensor in these reduction ops.
    * The following code can be compiled, but will raise a `c10::Error` when executed. This code compiled and executed successfully in the prior release.
```cpp
at::Tensor out;  # Undefined Tensor
const at::Tensor a = at::randn({2, 2});
at::IntArrayRef dim = {1};
at::sum_out(out, a, dim);
# c10::Error: Expected a Tensor of type Variable but found an undefined Tensor for argument #4 'out'
```

* **The C++ API utility functions `expand_inplace` and `expand_outplace` now return `c10::MaybeOwned<Tensor>` instead of `std::tuple<Tensor>`** ([#55065](https://github.com/pytorch/pytorch/pull/55065), [#55245](https://github.com/pytorch/pytorch/pull/55245)). 
The rationale for this change is to avoid unnecessary Tensor creation, thus improving performance. Functions in ExpandUtils return `c10::MaybeOwned<Tensor>` because expansion may not actually be needed, in which case we can improve efficiency by returning `c10::MaybeOwned<Tensor>::borrowed(to_expand)`. However, this means that you need to be careful: the returned `c10::MaybeOwned<Tensor> `must not outlive the original `Tensor` object that `to_expand` referred to! The deleted rvalue reference overloads of these functions help with this by preventing trivial use of a temporary resulting from a function call, but it is still possible to make a mistake. 

## TorchScript

* **Added recursive scripting for class type module attributes** ([#55124](https://github.com/pytorch/pytorch/pull/55124)).
    * This change is BC-breaking because it will result in class type module attributes being scripted when a module instance is scripted. In previous versions, such attributes were ignored unless their class type was also marked with `@torch.jit.script`. This new feature attempts to script the type, and falls back to the old behaviour of marking the class type attribute as "failed" if scripting fails. However, if the class definition does not have type annotations, the definition of the scripted class can different from users might expect (see code sample). If needed, users can explicitly disable the scripting of a class type attribute by adding its name to the `__jit_ignored_attributes__` class attribute of the module being scripted.

1.8.1:
```python
class MyClass:
    def __init__(self, a):
        self.attr = a
        
class MyModule(torch.nn.Module):
    def __init__(self):
        self.attr = MyClass(4)
        
sm = torch.jit.script(MyModule())
```

1.9.0:
```python
class MyClass:
    def __init__(self, a):
        self.attr = a
        
class MyModule(torch.nn.Module):
    def __init__(self):
        self.attr = MyClass(4)
 
# RuntimeError: Could not cast attribute 'attr' to type Tensor: Unable to cast Python instance of type <class 'int'> to C++ type 'at::Tensor'         
sm = torch.jit.script(MyModule()) 
```

This error occurs because `MyClass` is automatically scripted, but `self.attr` is inferred to be a `Tensor` instead of an `int` because `a` is not annotated. To fix this, annotate `a` with the right type `int`, or mark `attr` as an attribute that should be ignored by the scripting process and not recursively processed:
```python
       class MyModule(torch.nn.Module):
            __jit_ignored_attributes__ = ["attr"]
        
            def __init__(self):
                self.attr = MyClass(4)
```
                

## Quantization

*  **`torch.quantization.quantize_fx.convert_fx`’s `debug` argument has been changed to `is_reference` ([#52179](https://github.com/pytorch/pytorch/pull/52179)).**
<p align="center">
  <table align="center">
    <tr><th>1.8.1:</th><th>1.9.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
import torch.quantization.quantize_fx as quantize_fx
>>> m = quantize_fx.convert_fx(m, debug=True)
(Runs successfully)
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> m = quantize_fx.convert_fx(m, is_reference=True) # Runs successfully
>>> m = quantize_fx.convert_fx(m, debug=True)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: convert_fx() got an unexpected keyword argument 'debug'
      </pre></sub></td>
    </tr>
  </table>
</p>

* **`torch.cat` is now quantized to `torch.cat` instead of `torch.ops.quantized.cat` ([#54924](https://github.com/pytorch/pytorch/pull/54924)).**
Previously, we produced torch.ops.quantize.cat which took inputs, dequantized them
        and requantized them with new qparams. This behavior has been changed to produce `torch.cat` directly. [torch.cat](http://torch.cat/) uses the same observer/fake_quant instance for all inputs and output, assumes all inputs are sharing the same qparam, and produces a quantized Tensor with
        the same qparam as all inputs. Using torch.cat is expected to be more efficient since it does not introduce extra quant/dequant.
    * Version 1.8.1: `torch.cat` was quantized to  `torch.ops.quantized.cat.`
    * Version 1.9: `torch.cat` is quantized to `torch.cat` (`torch.cat` works on both floating point and quantized Tensor).

## Distributed

* **`DistributedDataParallel`: Removed support for inter-process device replication in DDP ([#54454](https://github.com/pytorch/pytorch/pull/54454),  [#54825](https://github.com/pytorch/pytorch/pull/54825), [#54826](https://github.com/pytorch/pytorch/pull/54826), [#55212](https://github.com/pytorch/pytorch/pull/55212), [#55253](https://github.com/pytorch/pytorch/pull/55253)`, `[`#55353`](https://github.com/pytorch/pytorch/pull/55353)).**
`DistributedDataParallel` now errors out when users attempt to use it in single-process multi-device mode, where a module is replicated across more than one device in a single process. This mode had been previously deprecated and is now removed. Use cases should switch to spawning a single process for each device that is used in replication, which is the performant way to use `DistributedDataParallel` and supports a variety of newly developed features.

1.8.1:
```python
>>> # Assume the below is ran on 2 ranks in a distributed setting.
>>> rank_to_devices = { 0: [0, 1], 1: [2, 3] }
>>> # Each rank replicates model across 2 GPUs.
>>> model_ddp = torch.nn.parallel.DistributedDataParallel(
        model,
        device_ids=rank_to_devices[rank]
    )
>>> # No error is raised, but below warning is produced.
>>> UserWarning: Single-Process Multi-GPU is not the recommended mode for DDP. In this mode, each DDP instance operates on multiple devices and creates multiple module replicas within one process. The overhead of scatter/gather and GIL contention in every forward pass can slow down training. Please consider using one DDP instance per device or per module replica by explicitly setting device_ids or CUDA_VISIBLE_DEVICES.
```

1.9.0:
```python
>>> # Assume the below is ran on 2 ranks in a distributed setting.
>>> rank_to_devices = { 0: [0, 1], 1: [2, 3] }
>>> # Each rank replicates model across 2 GPUs.
>>> model_ddp = torch.nn.parallel.DistributedDataParallel(
        model,
        device_ids=rank_to_devices[rank]
    )
>>> # Single process multi-GPU mode now produces an error on initialization.
>>> ValueError: device_ids can only be None or contain a single element.
```

* **`torch.distributed.elastic`: Replaced `torch.distributed.launch` with `torch.distributed.elastic_launch` ([#56037](https://github.com/pytorch/pytorch/pull/56037)`, `[`#56214`](https://github.com/pytorch/pytorch/pull/56214)).**
        * --logdir → —log_dir. The stdout and stderr log dir arg name and destination changed. The file destination changed from `$logdir/node_{}_local_rank_{}_stdout` to  `$log_dir/$rank/stdout.log`. If users used the `—logdir` introduced in 1.8 pytorch version, they need to use` —log_dir` parameter now.

1.8.1:
```python
#!/bin/bash
# Assumes training script train.py exists.
python -m torch.distributed.launch --nproc_per_node=2 --nnodes=1 --node_rank=0 --master_addr="127.0.0.1" --master_port="29500" --logdir test_logdir train.py
# Logs are written to $logdir/node_{}_local_rank_{}_stdout
```
1.9.0:
```python
#!/bin/bash
# Assumes training script train.py exists.
python -m torch.distributed.launch --nproc_per_node=2 --nnodes=1 --node_rank=0 --master_addr="127.0.0.1" --master_port="29500" --log_dir test_logdir train.py
# Logs are written to $log_dir/$rank/stdout.log
```

# Deprecations

## Python API

* **`torch.floor_divide` has been deprecated in favor of `torch.div(..., rounding_mode=‘floor’)` ([#50281](https://github.com/pytorch/pytorch/pull/50281)).**
    * `torch.floor_divide` incorrectly divides then truncates (rounds towards zero) instead of dividing then flooring (rounds “down”). Use the `rounding_mode` argument of `torch.div` to indicate if you’d like to continue performing truncation division or floor division, instead, since `torch.floor_divide` will be removed in a future PyTorch release.
* **Older linear algebra operations have been deprecated in favor of their new linalg module counterparts. Namely:**
    *  `torch.{cholesky, qr, symeig, chain_matmul, solve, eig, matrix_rank, lstsq}` have been deprecated in favor of `torch.linalg.{cholesky, qr, symeig, chain_matmul, solve, eig, matrix_rank, lstsq}` ([#57725,](https://github.com/pytorch/pytorch/pull/57725)[#57745](https://github.com/pytorch/pytorch/pull/57745), [#57732,](https://github.com/pytorch/pytorch/pull/57732)[#53453](https://github.com/pytorch/pytorch/pull/53453), [#57741](https://github.com/pytorch/pytorch/pull/57741), [#57727](https://github.com/pytorch/pytorch/pull/57727), [#57734](https://github.com/pytorch/pytorch/pull/57734), [#57743](https://github.com/pytorch/pytorch/pull/57743)).
    * `torch.norm` has been deprecated in favor of the new linalg module norm functions: `torch.linalg.vector_norm`, `torch.linalg.matrix_norm`, and `torch.linalg.norm` ([#57986](https://github.com/pytorch/pytorch/pull/57986)).
    * Aliased `torch.det`, `torch.slogdet`, `torch.matrix_power`, `torch.inverse`, and `torch.pinverse` to their linalg module counterparts ([#57821](https://github.com/pytorch/pytorch/pull/57821)).

## Autograd

* **[cpp] Renamed `AutoNonVariableTypeMode` to `AutoDispatchBelowAutograd` and added a warning. ([#56422](https://github.com/pytorch/pytorch/pull/56422))** 
`AutoNonVariableTypeMode` is deprecated and will be removed in 1.10 release. For kernel implementations,  please use `AutoDispatchBelowAutograd` instead. Check out more details on how to migrate your kernel [here](https://pytorch.org/cppdocs/notes/inference_mode.html#migration-guide-from-autononvariabletypemode). If you are looking for a user-facing API to enable running your inference-only workload, please use `c10::InferenceMode`. Using `AutoDispatchBelowAutogradMode` in user code is under risk of producing silently wrong result for some edge cases.
    
1.8.1:
```cpp
{
  at::AutoNonVariableTypeMode guard(true);
}
```

1.9.0:
```
{
  c10::AutoDispatchBelowAutograd guard(true); // for kernel implementations
  // c10::InferenceMode guard(true); --> consider inference mode if you are looking for a user-facing API

}
```

* **Removed logic for old style custom autograd `Function` ([#57357](https://github.com/pytorch/pytorch/pull/57357)).**
Instantiating a custom autograd function is now deprecated and will raise a warning. Users should call `.apply()` on the class itself because it is a static method.

1.8.1:
```python
        # Instantiating custom function will raise a warning in 1.9
        Func().apply
```

1.9.0:
```python
        # You should directly call the `apply` (classmethod) on the class
        Func.apply
```

* **Deprecated `get_analytical_jacobian` and `get_numerical_jacobian` ([#54378](https://github.com/pytorch/pytorch/pull/54378), [#54049](https://github.com/pytorch/pytorch/pull/54049)).**
`torch.autograd.gradcheck.get_analytical_jacobian`  and `torch.autograd.gradcheck.get_numerical_jacobian` are internal-facing functions that are not a part of our public API. We’ve refactored some PyTorch internals to work without it and will
        remove it in a future release. For gradient checking purposes, please use `torch.autograd.gradcheck`. 

## C++ API

* **Removed the redundant `linalg_` prefix from `torch::linalg::linalg_det` and `torch::linalg::linalg_norm` C++ API ([#57464](https://github.com/pytorch/pytorch/pull/57464)).**
C++ code that used to call `torch::linalg::{linalg_det, linalg_norm}` should be updated to call `torch::linalg::{det, norm}`

## Distributed

* **`torch.distributed.rpc`: Added a warning message to retire ProcessGroup RPC backend ([#55616](https://github.com/pytorch/pytorch/pull/55616))**
    * ProcessGroup RPC backend is being deprecated and 1.9 is the last release which will carry it. The default RPC backend is TensorPipe which is the recommended backend to use over ProcessGroup.

# 

# New features

### Python API

* Added BFloat16 support for `torch.{ceil, floor, frac, round, trunc, lerp, roll, diag, logaddexp, logaddexp2, nan_to_num, exp2, expm1, rsqrt, erfc, atan2, hypot}` on CUDA ([#57910](https://github.com/pytorch/pytorch/pull/57910), [#57907](https://github.com/pytorch/pytorch/pull/57907), [#57916](https://github.com/pytorch/pytorch/pull/57916), [#57908](https://github.com/pytorch/pytorch/pull/57908), [#58063](https://github.com/pytorch/pytorch/pull/58063), [#57913](https://github.com/pytorch/pytorch/pull/57913), [#57905](https://github.com/pytorch/pytorch/pull/57905)).
* Added `torch.pow()` for `torch.{float16, BFloat16}` on CPU ([#55280](https://github.com/pytorch/pytorch/pull/55280)).
* Added `torch.{index_select, argmax, argmin, min, max, amin, amax}` for `torch.{float16, BFloat16}` ([#53898](https://github.com/pytorch/pytorch/pull/53898), [#52582](https://github.com/pytorch/pytorch/pull/52582), [#51244](https://github.com/pytorch/pytorch/pull/51244), [#52579](https://github.com/pytorch/pytorch/pull/52579)).
* Added `torch.dot` for `BFloat16` on CUDA ([#57903](https://github.com/pytorch/pytorch/pull/57903)).
* Added support for tensor inputs for `min` and `max` arguments in `torch.clamp` ([#52695](https://github.com/pytorch/pytorch/pull/52695), [#56367](https://github.com/pytorch/pytorch/pull/56367)).
* Added a new `torch.special` namespace similar to `scipy.special` ([#52296](https://github.com/pytorch/pytorch/pull/52296)).
    * Added special.{`entr` ([#53500](https://github.com/pytorch/pytorch/pull/53500)),  `xlog1py` ([#55138](https://github.com/pytorch/pytorch/pull/55138)), `i0e` ([#54409](https://github.com/pytorch/pytorch/pull/54409)), `erfc`, `erfinv` ([#53260](https://github.com/pytorch/pytorch/pull/53260))}.
    * Added aliases for `special.{expm1, exp2}` ([#54670](https://github.com/pytorch/pytorch/pull/54670)).
    * Added aliases for `special.{sigmoid, logit}` ([#54759](https://github.com/pytorch/pytorch/pull/54759)).
* Added the following new operators in PyTorch similar to those in NumPy:
    * `torch.gradient` ([#54617](https://github.com/pytorch/pytorch/pull/54617))
    * `torch.{hsplit, vsplit, dsplit}` ([#53536](https://github.com/pytorch/pytorch/pull/53536))
    * `torch.positive` ([#55891](https://github.com/pytorch/pytorch/pull/55891))
    * `torch.frexp` ([#51097](https://github.com/pytorch/pytorch/pull/51097))
    * `torch.take_along_dim` ([#52833](https://github.com/pytorch/pytorch/pull/52833))
* Added a new keyword argument `alpha` to `torch.index_add` ([#54176](https://github.com/pytorch/pytorch/pull/54176)).
* Added `torch.assert_async` ([#53086](https://github.com/pytorch/pytorch/pull/53086))
* Added a new keyword argument `interpolation` to `torch.quantile` ([#49267](https://github.com/pytorch/pytorch/pull/49267)).
* Add correction parameter to std/var ([#50903](https://github.com/pytorch/pytorch/pull/50903))
* Added overloads for `torch.{std, var, std_mean, var_mean}` with a correction argument specifying the difference between the sample size and number of degrees of freedom. 
* Add support for integer type for `torch.`{`logit, rad2deg, deg2rad, polygamma}` ([#52028](https://github.com/pytorch/pytorch/pull/52028), [#51853,](https://github.com/pytorch/pytorch/pull/51853)[#57462](https://github.com/pytorch/pytorch/pull/57462))
* Added support for stable sort algorithm on CPU by a new kwarg `stable` ([#51790](https://github.com/pytorch/pytorch/pull/51790)).
* The `torch.linalg` module, analogous to NumPy’s linalg module but with several additional functions, is stable! Added `torch.linalg.{multi_dot, lstsq, vector_norm, matrix_norm, matrix_power, det, eig, eigvals, svdvals, cholesky_ex, inv_ex}` ([#51807](https://github.com/pytorch/pytorch/pull/51807), [#49093](https://github.com/pytorch/pytorch/pull/49093), [#51099](https://github.com/pytorch/pytorch/pull/51099), [#57127](https://github.com/pytorch/pytorch/pull/57127), [#52608](https://github.com/pytorch/pytorch/pull/52608), [#53119](https://github.com/pytorch/pytorch/pull/53119), [#52491](https://github.com/pytorch/pytorch/pull/52491), [#56684](https://github.com/pytorch/pytorch/pull/56684), [#56724](https://github.com/pytorch/pytorch/pull/56724), [#58039](https://github.com/pytorch/pytorch/pull/58039)).
* Added a new `device=meta` API ([#53143](https://github.com/pytorch/pytorch/pull/53143))
    * “meta” is a new device, like CPU/CUDA, that doesn’t allocate any memory for data. Operators that are passed meta tensor inputs will perform shape inference, without running the actually kernel computation. For example, `torch.ones(2, device='meta') + torch.ones(1, 2, device='meta')` will return a new meta tensor of size `[1, 2]` (performing broadcasting), without allocating memory or running an actual kernel.
    * `device=meta` API is implemented for `upsample_linear1d`([#51917](https://github.com/pytorch/pytorch/pull/51917)), `upsample_bilinear2d` and `upsample_bicubic2d` ([#52012](https://github.com/pytorch/pytorch/pull/52012)), `upsample_nearest3d` ([#52065](https://github.com/pytorch/pytorch/pull/52065)), `sin`([#52277](https://github.com/pytorch/pytorch/pull/52277)), `mul`([#52692](https://github.com/pytorch/pytorch/pull/52692)), `pow`([#53669](https://github.com/pytorch/pytorch/pull/53669)), `sub`([#53679](https://github.com/pytorch/pytorch/pull/53679)), `div`([#53680](https://github.com/pytorch/pytorch/pull/53680)), `copysign`([#55040](https://github.com/pytorch/pytorch/pull/55040)), `atan2`([#55130](https://github.com/pytorch/pytorch/pull/55130)), `sinh`([#55538](https://github.com/pytorch/pytorch/pull/55538)), `acosh`([#55540](https://github.com/pytorch/pytorch/pull/55540)), `cosh`([#55563](https://github.com/pytorch/pytorch/pull/55563)), `cos` ([#55564](https://github.com/pytorch/pytorch/pull/55564)), `replication_padding1d` ([#55481](https://github.com/pytorch/pytorch/pull/55481)), `replication_padding3d` ([#55499](https://github.com/pytorch/pytorch/pull/55499)), `replication_pad1d_backward` ([#55537](https://github.com/pytorch/pytorch/pull/55537)), `fractional_max_pool2d` ([#55581](https://github.com/pytorch/pytorch/pull/55581)), `reflection_pad1d` ([#55531](https://github.com/pytorch/pytorch/pull/55531)), `replication_pad2d` ([#55511](https://github.com/pytorch/pytorch/pull/55511)), `addmv` ([#55746](https://github.com/pytorch/pytorch/pull/55746)), all unary float functions ([#56082](https://github.com/pytorch/pytorch/pull/56082)), `adaptive_max_pool2d`([#56317](https://github.com/pytorch/pytorch/pull/56317)), `adaptive_max_pool3d` ([#56320](https://github.com/pytorch/pytorch/pull/56320)), all non-float unary operators (and `rsqrt`) ([#56151](https://github.com/pytorch/pytorch/pull/56151)), `adaptive_max_pool2d_backward` ([#56799](https://github.com/pytorch/pytorch/pull/56799)), `adaptive_max_pool3d_backward` ([#56800](https://github.com/pytorch/pytorch/pull/56800)), `neg`([#57212](https://github.com/pytorch/pytorch/pull/57212)), `max_pool2d_with_indices`([#56459](https://github.com/pytorch/pytorch/pull/56459)), `trunc` ([#57350](https://github.com/pytorch/pytorch/pull/57350)), `floor` ([#57587](https://github.com/pytorch/pytorch/pull/57587)), `sign` ([#57588](https://github.com/pytorch/pytorch/pull/57588)), `ceil` ([#57589](https://github.com/pytorch/pytorch/pull/57589)), `gcd` ([#57624](https://github.com/pytorch/pytorch/pull/57624)), `nextafter` ([#57625](https://github.com/pytorch/pytorch/pull/57625)), `igamma` and `igammac`([#57626](https://github.com/pytorch/pytorch/pull/57626)), `hypot`([#57627](https://github.com/pytorch/pytorch/pull/57627)), `lcm` ([#57628](https://github.com/pytorch/pytorch/pull/57628)), `logaddexp` and `logaddexp2` ([#57629](https://github.com/pytorch/pytorch/pull/57629)), `maximum` and `minimum` ([#57630](https://github.com/pytorch/pytorch/pull/57630)), `topk` ([#57790](https://github.com/pytorch/pytorch/pull/57790)), `max_pool2d_with_indices_backward` ([#57797](https://github.com/pytorch/pytorch/pull/57797)), `threshold` ([#57810](https://github.com/pytorch/pytorch/pull/57810)), `addmm` ([#57417](https://github.com/pytorch/pytorch/pull/57417)), `heaviside` ([#57933](https://github.com/pytorch/pytorch/pull/57933)), `elu`([#57619](https://github.com/pytorch/pytorch/pull/57619)), `softplus` ([#57620](https://github.com/pytorch/pytorch/pull/57620)), `leaky_relu` ([#57621](https://github.com/pytorch/pytorch/pull/57621)), `hardsigmoid` ([#57622](https://github.com/pytorch/pytorch/pull/57622)), `softshrink` ([#57623](https://github.com/pytorch/pytorch/pull/57623)), `silu` ([#58050](https://github.com/pytorch/pytorch/pull/58050)), `empty_strided` ([#53397](https://github.com/pytorch/pytorch/pull/53397)), non-composite in-place operators ([#54901](https://github.com/pytorch/pytorch/pull/54901))

### Complex Numbers

* Added complex autograd support for `torch.{masked_fill, polar, cumsum, lerp, prod, rsub, unfold, symeig, index_copy}` ([#52483](https://github.com/pytorch/pytorch/pull/52483), [#52488](https://github.com/pytorch/pytorch/pull/52488), [#53240](https://github.com/pytorch/pytorch/pull/53240), [#53689](https://github.com/pytorch/pytorch/pull/53689), [#48125](https://github.com/pytorch/pytorch/pull/48125), [#53702](https://github.com/pytorch/pytorch/pull/53702), [#52999](https://github.com/pytorch/pytorch/pull/52999), [#55085](https://github.com/pytorch/pytorch/pull/55085), [#52203](https://github.com/pytorch/pytorch/pull/52203)).
* Added complex support for torch.lerp ([#54129](https://github.com/pytorch/pytorch/pull/54129)) and torch.sigmoid ([#55975](https://github.com/pytorch/pytorch/pull/55975)) on CUDA. 
* Added complex support for `torch.index_copy` and `torch.{take}` and `torch.Tensor.put_` on both CPU and CUDA ([#52203](https://github.com/pytorch/pytorch/pull/52203), [#53356](https://github.com/pytorch/pytorch/pull/53356)).
* Added complex support to TorchScript.
    * Added logic to teach TorchScript frontend to parse complex literals, and complex lists. ([#52881](https://github.com/pytorch/pytorch/pull/52881)).
    * Added TorchScript support for:
        *  complex constructor and `torch.{add, mul, sub, as_tensor}` ([#52881](https://github.com/pytorch/pytorch/pull/52881)).
        * `cmath` unary ops: `cmath.{phase, log, log10, sqrt, exp, sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, asinh, acosh, atanh}` ([#54089](https://github.com/pytorch/pytorch/pull/54089)).
        * `cmath.`{`infj, nanj}` ([#54328](https://github.com/pytorch/pytorch/pull/54328)).
        *  `cmath.{isinf, isnan, isfinite, rect}` ([#54541](https://github.com/pytorch/pytorch/pull/54541)).
        * real and imag tensor attributes (`tensor.real/imag`) ([#54692](https://github.com/pytorch/pytorch/pull/54692)).
    * Fixed `test_variant_consistency_jit_addmm` for complex types ([#54917](https://github.com/pytorch/pytorch/pull/54917), [#57129](https://github.com/pytorch/pytorch/pull/57129)).
* Added initial operator support for sparse complex tensors ([#57125](https://github.com/pytorch/pytorch/pull/57125)).
    * Added complex support for `torch.{sparse_coo_tensor, coalesce, to_dense, to_sparse, sparse_add, sspaddmm, saddmm}`.
* Added `torch.Tensor.{cfloat, cdouble}` functions ([#58137](https://github.com/pytorch/pytorch/pull/58137)).
* Added complex support for all reductions for `torch.{std, var}` to return a real valued output tensor for complex inputs ([#58066](https://github.com/pytorch/pytorch/pull/58066)) .
* Updated autograd formulas for many linear algebra operations support complex tensors:
    * `eig`: faster and with complex support ([#52875](https://github.com/pytorch/pytorch/pull/52875))
    * `lu`: more numerically stable and with complex support. ([#53994](https://github.com/pytorch/pytorch/pull/53994))

### torch.nn

* New `torch.nn` modules: `nn.LazyBatchNorm*d` ([#51862](https://github.com/pytorch/pytorch/pull/51862)), `nn.HuberLoss` ([#50553](https://github.com/pytorch/pytorch/pull/50553)), `nn.Mish` ([#58375](https://github.com/pytorch/pytorch/issues/58375)).
* New parametrization functionality ([#33344](https://github.com/pytorch/pytorch/pull/33344), [#58142](https://github.com/pytorch/pytorch/pull/58142), [#55456](https://github.com/pytorch/pytorch/pull/55456), [#57784](https://github.com/pytorch/pytorch/pull/57784)).
* `nn.Conv*d`: Added `padding='same'` mode for non-strided convolutions ([#45667](https://github.com/pytorch/pytorch/pull/45667)).
* `nn.EmbeddingBag`: Added `padding_idx` support ([#49237](https://github.com/pytorch/pytorch/pull/49237), [#56065](https://github.com/pytorch/pytorch/pull/56065), [#56618](https://github.com/pytorch/pytorch/pull/56618)).
* Added mish activation function ([#58648](https://github.com/pytorch/pytorch/pull/58648)).
* [memory format] Added channels last support for `MaxPool2d` ([#56361](https://github.com/pytorch/pytorch/pull/56361)).
* Added the option to build PyTorch with DNNL + AMD BLIS path ([#54953](https://github.com/pytorch/pytorch/pull/54953)).

### Profiler

* Added `skip_first` parameter to the default schedule ([#58025](https://github.com/pytorch/pytorch/pull/58025)).
* Added support for trace metadata ([#56575](https://github.com/pytorch/pytorch/pull/56575)).
* Added `gzip` format support for chrome tracing ([#56554](https://github.com/pytorch/pytorch/pull/56554)).
* Added `sequenceNr` and `fwdThreadId` to the trace ([#57182](https://github.com/pytorch/pytorch/pull/57182)).
* Enabled Kineto in CPU builds ([#53174](https://github.com/pytorch/pytorch/pull/53174)).

### Autograd

* Added new inference mode both in C++ ([](https://github.com/pytorch/pytorch/pull/58045)[#54403](https://github.com/pytorch/pytorch/pull/54403), [#53343](https://github.com/pytorch/pytorch/pull/53343)) and python ([#58045](https://github.com/pytorch/pytorch/pull/58045), [#57480](https://github.com/pytorch/pytorch/pull/57480)).
* Added `fast_mode` argument to `autograd.gradcheck` ([#54480](https://github.com/pytorch/pytorch/pull/54480)).
* Added support for non-Tensor inputs and outputs to `torch.utils.checkpoint` functions ([#52422](https://github.com/pytorch/pytorch/pull/52422)).

### Dataloader

* Implemented `FilterIterDataPipe` ([#51783](https://github.com/pytorch/pytorch/pull/51783)).
* Added context manager for runtime type validation ([#55936](https://github.com/pytorch/pytorch/pull/55936)).
* Added typing enforcement for `DataPipe` at construct-time ([#54066](https://github.com/pytorch/pytorch/pull/54066)).
* Added typing Enforcement for `DataPipe` at runtime ([#54544](https://github.com/pytorch/pytorch/pull/54544)).
* Implemented `issubtype` for `DataLoader` type hints ([#54299](https://github.com/pytorch/pytorch/pull/54299)).
* Added type hint for SequentialSampler ([#56374](https://github.com/pytorch/pytorch/pull/56374)).
* Added `ConcatDataPipe` ([#53301](https://github.com/pytorch/pytorch/pull/53301)).
* Introduced deterministic context to `DataLoader` ([#53271](https://github.com/pytorch/pytorch/pull/53271)).
* Added `ZipIterDataPipe` ([#53554](https://github.com/pytorch/pytorch/pull/53554)).
* Added switch to guaranteed determinism & add option to non_deterministic ([#53532](https://github.com/pytorch/pytorch/pull/53532)).
* Added `TransformsIterDataPipe` ([#52604](https://github.com/pytorch/pytorch/pull/52604)).
* Renamed Callable to `MapIterDataPipe` ([#51879](https://github.com/pytorch/pytorch/pull/51879)).

### CUDA

* Added the following new features to CUDA Graphs:
    *  Private mempools ([#54038](https://github.com/pytorch/pytorch/pull/54038))
    * Support for RNN capture when cuDNN dropout is used ([#57373](https://github.com/pytorch/pytorch/pull/57373)).
* Added support for `'max'` reduction for `torch.segment_reduce` ([#56704](https://github.com/pytorch/pytorch/pull/56704)).
* Added support for CUDA allocator to handle multiple streams seamlessly ([#55860](https://github.com/pytorch/pytorch/pull/55860)).

### C++ API

* Added `torch::nn::functional::huber_loss` ([#50553](https://github.com/pytorch/pytorch/pull/50553)).
* Added learning rate schedulers to C++ API ([#52268](https://github.com/pytorch/pytorch/pull/52268)).
* Added `padding='same'` mode to `torch::conv{1,2,3}d` ([#45667](https://github.com/pytorch/pytorch/pull/45667)).
* Added `padding_idx` argument to `EmbeddingBag` ([#49237](https://github.com/pytorch/pytorch/pull/49237)).
* Added mish activation function ([#58648](https://github.com/pytorch/pytorch/pull/58648)) ([#58940](https://github.com/pytorch/pytorch/pull/58940)).

### TorchScript

* Added reductions to NNC python bindings ([#52492](https://github.com/pytorch/pytorch/pull/52492)).
* Added Python bindings for ExternalCalls. ([#52905](https://github.com/pytorch/pytorch/pull/52905)).
* Added an API to reorder multiple loops ([#55568](https://github.com/pytorch/pytorch/pull/55568)).
* Added NNC support for `pow` on CPU ([#56308](https://github.com/pytorch/pytorch/pull/56308)).
* Enabled horizontal fusion of all loops ([#56324](https://github.com/pytorch/pytorch/pull/56324)).
* Added an API for Buffer Compression ([#55853](https://github.com/pytorch/pytorch/pull/55853)).
* Added API to distribute loops ([#53865](https://github.com/pytorch/pytorch/pull/53865)).
* Added `matmul` for NNC lowering/unified dtypes ([#56456](https://github.com/pytorch/pytorch/pull/56456)).
* Added a method to compute `conv` without bias ([#57512](https://github.com/pytorch/pytorch/pull/57512)).
* Added support for computing `conv` with dynamic shapes ([#57514](https://github.com/pytorch/pytorch/pull/57514)).
* Added NNC lowerings for `t`/`transpose`/`permute`/`expand` ([#57426](https://github.com/pytorch/pytorch/pull/57426)).
* Updated external functions for mobile build ([#56850](https://github.com/pytorch/pytorch/pull/56850)).
* Added `GELU` To NNC ([#57753](https://github.com/pytorch/pytorch/pull/57753)).
* Implemented `GELU` Backward ([#58249](https://github.com/pytorch/pytorch/pull/58249)).
* Added a mobile NNC backend skeleton ([#56852](https://github.com/pytorch/pytorch/pull/56852)).
* Added support for `torch.type` ([#51904](https://github.com/pytorch/pytorch/pull/51904))
* Added `dict()` constructor ([#51934](https://github.com/pytorch/pytorch/pull/51934)).
* Added a new `torch::deploy` to manage multiple python interpreters in a single
    process to deploy PyTorch models packaged with torch.package ([#51754](https://github.com/pytorch/pytorch/pull/51754)).
* Reintroduced static dispatch ([#51957](https://github.com/pytorch/pytorch/pull/51957)).
* Added TS support for `torch.any` ([#52360](https://github.com/pytorch/pytorch/pull/52360)).
* Added a demo backend with compiler ([#52603](https://github.com/pytorch/pytorch/pull/52603)).
* Added MKLDNN fuser ([#51600](https://github.com/pytorch/pytorch/pull/51600)).
* Added a context manager for hiding source ranges ([#53188](https://github.com/pytorch/pytorch/pull/53188)).
* Implemented `embedding_bag` for SR ([#52429](https://github.com/pytorch/pytorch/pull/52429)).
* Allowed the use of `AliasDb` in Python ([#51336](https://github.com/pytorch/pytorch/pull/51336)).
* Added support for `DictConstruct` ([#54438](https://github.com/pytorch/pytorch/pull/54438))
* Added `sliceHead`/`sliceTail` APIs with short parameter list ([#55115](https://github.com/pytorch/pytorch/pull/55115)).
* Added logic to infer argument types in TorchScript ([#56832](https://github.com/pytorch/pytorch/pull/56832)).
* Added support for  custom Python classes in `CUDAFuture` ([#56516](https://github.com/pytorch/pytorch/pull/56516)).
* Added a concat optimization pass ([#55474](https://github.com/pytorch/pytorch/pull/55474)).
* Added initial support for PEP-585 types ([#57363](https://github.com/pytorch/pytorch/pull/57363)).
* Added logic to infer types for arguments of methods not invoked directly by `MonkeyType` ([#57202](https://github.com/pytorch/pytorch/pull/57202)).
* Added support for `torch.jit.ignore` as a context manager ([#55172](https://github.com/pytorch/pytorch/pull/55172)).
* Implemented `hardswish`/`hardsigmoid `on MKLDNN tensors ([#55218](https://github.com/pytorch/pytorch/pull/55218)).
* Added `model_dump` tool for model inspection ([#56868](https://github.com/pytorch/pytorch/pull/56868))
* Added static method support for TorchBind ([#51177](https://github.com/pytorch/pytorch/pull/51177))
* Added TS support for `pow` ([#52374](https://github.com/pytorch/pytorch/pull/52374))
* Added support for default argument values to `TorchBind` ([#51253](https://github.com/pytorch/pytorch/pull/51253)).
* Added support for AST rewriting for submodules ([#52297](https://github.com/pytorch/pytorch/pull/52297)).
* Added `optimize_for_inference` API ([#58193](https://github.com/pytorch/pytorch/pull/58193)).
* Registered `aten::index_out` ([#51742](https://github.com/pytorch/pytorch/pull/51742)).
* Added `PYTORCH_TENSOREXPR_DONT_FUSE` env variable to disable fusion on specified operators ([#55650](https://github.com/pytorch/pytorch/pull/55650)).

### torch.package

* Allow TorchScript models to be contained in the package format ([#54891,](https://github.com/pytorch/pytorch/pull/54891)[#56299,](https://github.com/pytorch/pytorch/pull/56299)[#54893](https://github.com/pytorch/pytorch/pull/54893), [#57573](https://github.com/pytorch/pytorch/pull/57573), [#54894](https://github.com/pytorch/pytorch/pull/54894), [#57678](https://github.com/pytorch/pytorch/pull/57678)).

### Mobile

* Added 8x1 block sparse kernels for ARM and AArch64 ([#51118](https://github.com/pytorch/pytorch/pull/51118), [#51119](https://github.com/pytorch/pytorch/pull/51119), [#51120](https://github.com/pytorch/pytorch/pull/51120)).
* Made NNAPI converter handle binary ops combining NHWC+NCHW in some cases ([#48812](https://github.com/pytorch/pytorch/pull/48812)).
* Improved support for multiple inputs and outputs in NNAPI ([#54697](https://github.com/pytorch/pytorch/pull/54697)).
* Added flexible size support for NNAPI ([#54701](https://github.com/pytorch/pytorch/pull/54701)).
* Added new ops for Metal (concat, mul/sub/div, transpose, view, reshape, mean, chunk, reflection_pad2d) ( [#53950](https://github.com/pytorch/pytorch/pull/53950), [#54107](https://github.com/pytorch/pytorch/pull/54107), [#54522](https://github.com/pytorch/pytorch/pull/54522), [#56073](https://github.com/pytorch/pytorch/pull/56073), [#56074](https://github.com/pytorch/pytorch/pull/56074), [#58263](https://github.com/pytorch/pytorch/pull/58263)).
* Added python binding to use mobile cpu allocator ([#52323](https://github.com/pytorch/pytorch/pull/52323)).
* Added lightweight RandomSampler for mobile ([#58201](https://github.com/pytorch/pytorch/pull/58201)).
* Added support for:
    * new ops to NNAPI converter (size, unsqueeze, cat, mean) ([#52026](https://github.com/pytorch/pytorch/pull/52026), [#48811](https://github.com/pytorch/pytorch/pull/48811)).
    * multi-dimension tensors in Metal via MPSImage ([#54106](https://github.com/pytorch/pytorch/pull/54106)).
    * multiple output tensors in Metal ([#56072](https://github.com/pytorch/pytorch/pull/56072)).
    * methods other than forward in optimize_for_mobile  ([#53314](https://github.com/pytorch/pytorch/pull/53314)).
    * ChannelsLast in TensorImageUtils on Android ([#48990](https://github.com/pytorch/pytorch/pull/48990)).
    * loading “extra files” in Java/Android ([#55644](https://github.com/pytorch/pytorch/pull/55644)).
    * loading “extra files” in Lite interpreter ([#52635](https://github.com/pytorch/pytorch/pull/52635)).
    * querying bytecode version in Lite interpreter and bytecode models ([#56948](https://github.com/pytorch/pytorch/pull/56948), [#56948](https://github.com/pytorch/pytorch/pull/56948)).
    * exporting some older bytecode versions for Lite interpreter ([#56802](https://github.com/pytorch/pytorch/pull/56802)).
    * querying available ops ([#57570](https://github.com/pytorch/pytorch/pull/57570)).
* Added SqueezeNet to PyTorch Playground (71d0b5632b).
* Added libtorch lite build ([#51419](https://github.com/pytorch/pytorch/pull/51419)).

### Distributed

* `torch.distributed.Store`
    * Added `compare_set` op ([#51815](https://github.com/pytorch/pytorch/pull/51815)).
    * Added new `watchKey` method to register callbacks on a key ([#56217](https://github.com/pytorch/pytorch/pull/56217)).
* `torch.distributed.rpc`
    * Allowed passing `cpu` to CUDA RPC device maps ([#57019](https://github.com/pytorch/pytorch/pull/57019)).
    *  Add a new `devices` argument to TensorPipe options to specify set of devices for TensorPipe ([#56405](https://github.com/pytorch/pytorch/pull/56405))
* `DistributedDataParallel`
    * Adds a flag to ddp `join` context manager that enables throwing an error across all ranks when this flag is specified ([#56755](https://github.com/pytorch/pytorch/pull/56755))
    * Enable static graph training in DDP ([#55248](https://github.com/pytorch/pytorch/pull/55248), [#54995](https://github.com/pytorch/pytorch/pull/54995))
    * Log unused parameter names in DDP when crashing due to unused parameters ([#55075](https://github.com/pytorch/pytorch/pull/55075))
    * Introduce `torch.distributed.algorithms.default_hooks.fp16_compress_wrapper` wrapper that can be combined with other communication hooks ([#53808](https://github.com/pytorch/pytorch/pull/53808))
    * Support loading a non-DP/DDP model from a DP/DDP state_dict ([#53224](https://github.com/pytorch/pytorch/pull/53224))
    * Enhanced logging in DDP for performance metrics ([#52957](https://github.com/pytorch/pytorch/pull/52957), [#53145](https://github.com/pytorch/pytorch/pull/53145), [#54647](https://github.com/pytorch/pytorch/pull/54647))
* `torch.distributed`
    * Support `work.result` API for MPI backend ([#57168](https://github.com/pytorch/pytorch/pull/57168))
    * Support `work.result` for `ProcessGroupGloo::AsyncWork` objects ([#57565](https://github.com/pytorch/pytorch/pull/57565))
    * Support `work.get_future()` API for ProcessGroupMPI and ProcessGroupGloo [(](https://github.com/pytorch/pytorch/pull/57818)[#57818,](https://github.com/pytorch/pytorch/pull/57818)[#57214](https://github.com/pytorch/pytorch/pull/57214))
    * New` torch.distributed.monitored_barrier` API (Gloo-only) ([#53773](https://github.com/pytorch/pytorch/pull/53773), [#53787](https://github.com/pytorch/pytorch/pull/53787), [#55009](https://github.com/pytorch/pytorch/pull/55009), [#55010](https://github.com/pytorch/pytorch/pull/55010), [#55197](https://github.com/pytorch/pytorch/pull/55197), [#55265](https://github.com/pytorch/pytorch/pull/55265), [#55989](https://github.com/pytorch/pytorch/pull/55989), [#55990](https://github.com/pytorch/pytorch/pull/55990))
    * Allow passing `options` field to process group initialization APIs ([#53662](https://github.com/pytorch/pytorch/pull/53662), [#54090](https://github.com/pytorch/pytorch/pull/54090), [#53663](https://github.com/pytorch/pytorch/pull/53663))
    * Enable profiling for distributed collectives ([#51822](https://github.com/pytorch/pytorch/pull/51822), , [#52004](https://github.com/pytorch/pytorch/pull/52004), [#52031](https://github.com/pytorch/pytorch/pull/52031), [#52949](https://github.com/pytorch/pytorch/pull/52949), [#55204](https://github.com/pytorch/pytorch/pull/55204), [#56412](https://github.com/pytorch/pytorch/pull/56412), [#56216](https://github.com/pytorch/pytorch/pull/56216), [#56427](https://github.com/pytorch/pytorch/pull/56427))
    * Allow user to specify `TORCH_DISTRIBUTED_DEBUG `environment variable ([#52481](https://github.com/pytorch/pytorch/pull/52481))
    * Added `compareSet` method for `torch.distributed.{HashStore, FileStore}` ([#53803](https://github.com/pytorch/pytorch/pull/53803)).
* Added new `torch.distributed.elastic `module that upstreams `pytorch/elastic`
    * Introduce RendezvousSettings ([#56537](https://github.com/pytorch/pytorch/pull/56537))
    * Introduce a new from_backend static constructor for DynamicRendezvousHandler ([#57150](https://github.com/pytorch/pytorch/pull/57150))
    * Introduce the implementation of DynamicRendezvousHandler ([#57151](https://github.com/pytorch/pytorch/pull/57151))
    * add support for the new error file format ([#57084](https://github.com/pytorch/pytorch/pull/57084))
    * Introduce the delay utility function ([#56533](https://github.com/pytorch/pytorch/pull/56533))
    *  Make torchelastic launcher compatible with the caffe2.distributed.launch ([#55687](https://github.com/pytorch/pytorch/pull/55687))
    * Introduce `PeriodicTimer` ([#55919](https://github.com/pytorch/pytorch/pull/55919))
    * Introduce `DynamicRendezvousHandler` and `RendezvousBackend`. ([#55635](https://github.com/pytorch/pytorch/pull/55635))
    * Introduce `C10dRendezvousBackend`. ([#55636](https://github.com/pytorch/pytorch/pull/55636))
    * Introduce `EtcdRendezvousBackend`. ([#55637](https://github.com/pytorch/pytorch/pull/55637))
    * Added `torch.distributed.elastic.launchers.api`, `torch.distributed.elastic.metrics`, `torch.distributed.events`, `torch.distributed.rendezvous`, `torch.distributed.elastic.agent` modules ([#55471](https://github.com/pytorch/pytorch/pull/55471), [#53870](https://github.com/pytorch/pytorch/pull/53870), [#53574](https://github.com/pytorch/pytorch/pull/53574), [#53760](https://github.com/pytorch/pytorch/pull/53760), [#53172](https://github.com/pytorch/pytorch/pull/53172), [#54343](https://github.com/pytorch/pytorch/pull/54343))
    * Upstreamed timer and multiprocessing classes to `torch.distribute.elastic.timer` and `torch.distributed.elastic.multiprocessing` ([#53574](https://github.com/pytorch/pytorch/pull/53574))
* `torch.distributed.nn.RemoteModule`: Enable RemoteModule to directly send GPU tensors over the wire on TensorPipe RPC backend if a device map is provided ([#57288](https://github.com/pytorch/pytorch/pull/57288))
* `torch.distributed.optim`: 
    * Allow `torch.optim.Adamax`  to be used as a TorchScript functional optimizer in RPC ([#55833](https://github.com/pytorch/pytorch/pull/55833))
    * Allow `torch.optim.Rprop` to be used as a TorchScript functional optimizer in RPC ([#55834](https://github.com/pytorch/pytorch/pull/55834))

### torch.fx

* Added `torch.fx.Node.format_node()` ([#51737](https://github.com/pytorch/pytorch/pull/51737)).
* Added a `Transformer` to normalize args/kwargs of `torch.nn.functional` calls into only kwargs ([#51816](https://github.com/pytorch/pytorch/pull/51816)).
* Added submodule manipulation APIs on `GraphModule` ([#52358](https://github.com/pytorch/pytorch/pull/52358)).
* Added `Graph.eliminate_dead_code` ([#52658](https://github.com/pytorch/pytorch/pull/52658)).
* Added a function to retrieve `inspect.Signature` instances for PyTorch operations ([#53830](https://github.com/pytorch/pytorch/pull/53830)).
* Experimental type annotation pass using Python signatures ([#53831](https://github.com/pytorch/pytorch/pull/53831)).
* Added a transformer to normalize `torch` namespace operations ([#53832](https://github.com/pytorch/pytorch/pull/53832)).
* Extended `NormalizeArgs` to work on `torch` namespace operations ([#54236](https://github.com/pytorch/pytorch/pull/54236)).
* Added FX `optimize_for_inference` for Intel CPUs ([#53805](https://github.com/pytorch/pytorch/pull/53805), [#58293](https://github.com/pytorch/pytorch/pull/58293)).
* Added a metadata dict to `Node` and switch shape-prop to use that ([#54926](https://github.com/pytorch/pytorch/pull/54926)).
* Added C-level monkey patching of `torch.randn` to capture it during tracing ([#54060](https://github.com/pytorch/pytorch/pull/54060)).
* Added a new API replace_input_with to `Node` ([#55887](https://github.com/pytorch/pytorch/pull/55887)).
* Added net splitter and net minimizer utilities ([#56201](https://github.com/pytorch/pytorch/pull/56201)).
* Added PyTree support to FX through `concrete_args` ([#55888](https://github.com/pytorch/pytorch/pull/55888)).
* Added support for proxy-able classes ([#56737](https://github.com/pytorch/pytorch/pull/56737)).

### ONNX

* Support onnxifi interface for set/get options ([#52388](https://github.com/pytorch/pytorch/pull/52388)).
* Support --onnxifi_min_ops in AOT flow ([#52380](https://github.com/pytorch/pytorch/pull/52380)).
* Redesign onnx pass to enable shape type dependent pattern conversion - cont ([#51795)](https://github.com/pytorch/pytorch/pull/51795) ([#53304)](https://github.com/pytorch/pytorch/pull/53304).
* Support inplace operations on inplace indexing ([#52063)](https://github.com/pytorch/pytorch/pull/52063) ([#53306](https://github.com/pytorch/pytorch/pull/53306)).
* Symbolic shape inference ([#51481](https://github.com/pytorch/pytorch/pull/51481)) ([#53307](https://github.com/pytorch/pytorch/pull/53307)).
* Support repeat_interleave symbolic ([#52855](https://github.com/pytorch/pytorch/pull/52855)) ([#53312](https://github.com/pytorch/pytorch/pull/53312)).
* Support primitive type input/outputs and attributes ([#53550](https://github.com/pytorch/pytorch/pull/53550)) ([#54864](https://github.com/pytorch/pytorch/pull/54864)).
* Support outer export to onnx ([#53603](https://github.com/pytorch/pytorch/pull/53603)) ([#54869](https://github.com/pytorch/pytorch/pull/54869)).
* Support hardsigmoid symbolic in opset 9 #49649 ([#54193](https://github.com/pytorch/pytorch/pull/54193)).
* Support support for hann_window operator ([#54587](https://github.com/pytorch/pytorch/pull/54587)) ([#56163](https://github.com/pytorch/pytorch/pull/56163)).
* Enable tensordot symbolic function ([#55654](https://github.com/pytorch/pytorch/pull/55654)) ([#56166](https://github.com/pytorch/pytorch/pull/56166)).
* Support for prim::min ([#55259](https://github.com/pytorch/pytorch/pull/55259)) ([#56168](https://github.com/pytorch/pytorch/pull/56168)).
* Support mv op ([#55470](https://github.com/pytorch/pytorch/pull/55470)) ([#56169](https://github.com/pytorch/pytorch/pull/56169)).
* Support .item() export & NumberType to tensor conversion ([#55697](https://github.com/pytorch/pytorch/pull/55697)) ([#57594](https://github.com/pytorch/pytorch/pull/57594)).
* Support a new operator for fill_() function ([#56859](https://github.com/pytorch/pytorch/pull/56859)) ([#57596](https://github.com/pytorch/pytorch/pull/57596)).
* Support index_add_ function ([#56867](https://github.com/pytorch/pytorch/pull/56867)) ([#57830](https://github.com/pytorch/pytorch/pull/57830)).
* Support tensor.to(device) ([#56857](https://github.com/pytorch/pytorch/pull/56857)) ([#57599](https://github.com/pytorch/pytorch/pull/57599)).
* Support registering custom export for prim::PythonOp from torch.autograd.Function ([#55630](https://github.com/pytorch/pytorch/pull/55630)) ([#57600](https://github.com/pytorch/pytorch/pull/57600)).

### Vulkan

* Added the `hardswish` and `hardsigmoid` activation functions ([#53362](https://github.com/pytorch/pytorch/pull/53362)).
* Added the `reflection_pad2d` op ([#53604](https://github.com/pytorch/pytorch/pull/53604)).
* Added an implementation of Winograd convolutions ([#54639](https://github.com/pytorch/pytorch/pull/54639)).
* Added the `sigmoid` activation function ([#57867](https://github.com/pytorch/pytorch/pull/57867)).

### Misc

* Android packages are now published to maven central ([#53568](https://github.com/pytorch/pytorch/pull/53568)).
* Kineto is now supported on Windows ([#56323](https://github.com/pytorch/pytorch/pull/56323)).
* Added a Gloo `TCP_TLS `transport ([#56442](https://github.com/pytorch/pytorch/pull/56442)).
* Add ability to collect minidumps after the crash ([#59236](https://github.com/pytorch/pytorch/pull/59236)).

# Improvements

### Python API

* Added nondeterministic alert for `index_put_` when `accumulate=False` ([#55827](https://github.com/pytorch/pytorch/pull/55827)).
* Added deterministic path for `torch.index_add` on CUDA ([#56521](https://github.com/pytorch/pytorch/pull/56521)).
* Added deterministic path for `torch.index_copy` on CPU ([#56900](https://github.com/pytorch/pytorch/pull/56900)).
* Removed beta warning for use_deterministic_algorithms ([#58074](https://github.com/pytorch/pytorch/pull/58074))
* Updated `torch.Tensor.unflatten` to be able to infer size value in `sizes` from -1 ([#51955](https://github.com/pytorch/pytorch/pull/51955)).
* Added a safe cast and copy for `out=` input tensor for `torch.tensordot` ([#56286](https://github.com/pytorch/pytorch/pull/56286)).
* Added cross-device check for `out` and `input` tensors for `torch.cat` ([#53004](https://github.com/pytorch/pytorch/pull/53004)).
* Modified the order of asserts to correct the error message when nan appears in `torch.multinomial` on CUDA ([#53288](https://github.com/pytorch/pytorch/pull/53288)).
* Converted a few more checks for unsupported device to raise `NotImplementedError` ([#53610](https://github.com/pytorch/pytorch/pull/53610)).
* Made shared cache thread-safe for `torch.multiprocessing` ([#53750](https://github.com/pytorch/pytorch/pull/53750)).
* Added support for `torch.int32` indices in `torch.repeat_interleave` ([#55102](https://github.com/pytorch/pytorch/pull/55102)).
* Added a check to give a clear error message when a binary function is called for  non-complex inputs with complex valued alpha ([#54964](https://github.com/pytorch/pytorch/pull/54964)).
* Propagate error message from `torch_shm_manager` when running `torch.multiprocessing` ([#57307](https://github.com/pytorch/pytorch/pull/57307), [#57310](https://github.com/pytorch/pytorch/pull/57310)).
* Enabled deterministic path for `index_copy_cud`a with index_put ([#58144](https://github.com/pytorch/pytorch/pull/58144)).
* Added support for uppercase letters in `torch.einsum` ([#56475](https://github.com/pytorch/pytorch/pull/56475)).
* Added CUDA support for `torch.orgqr` ([#51348](https://github.com/pytorch/pytorch/pull/51348)) and  `torch.ormqr` ([#57316](https://github.com/pytorch/pytorch/pull/57316)).
* Added support for batched as well as complex inputs for `torch.geqrf` on both CPU and CUDA ([#56249](https://github.com/pytorch/pytorch/pull/56249), [#56251](https://github.com/pytorch/pytorch/pull/56251)).

### Complex Numbers

* Fixed `torch.{linspace, logspace}` to correctly infer complex type and return a complex tensor when the `start` and (or) `end` values are complex numbers, and the `dtype` value is `None`  ([#38875](https://github.com/pytorch/pytorch/pull/38875)).

### Autograd

* Added support for single tensor in `inputs` argument for `.backward()` ([#53827](https://github.com/pytorch/pytorch/pull/53827)).
* Added support for C++ optional arguments in autograd custom functions ([#54270](https://github.com/pytorch/pytorch/pull/54270)).
* Added autograd support to `torch.orgqr` ([#52637](https://github.com/pytorch/pytorch/pull/52637)), `torch.segment_reduce` ([#56792](https://github.com/pytorch/pytorch/pull/56792)).
* Added deterministic backward for `torch.gather` for `dim=1` ([#55573](https://github.com/pytorch/pytorch/pull/55573)).
* Make detach return an alias even under inference mode ([#59633](https://github.com/pytorch/pytorch/pull/59633)).

### torch.nn

* Add 3D depthwise separable convolution ([#51027](https://github.com/pytorch/pytorch/pull/51027))
* Make bias in lazy modules lazy and avoid creating empty tensors ([#52212](https://github.com/pytorch/pytorch/pull/52212)).
* BFloat16: enable prepacked weights's inference ([#48922](https://github.com/pytorch/pytorch/pull/48922)).
* Enable mkldnn conv2d backward to support mkldnn tensor input ([#48994](https://github.com/pytorch/pytorch/pull/48994)).
* Add OneDNN pooling backward ([#49454](https://github.com/pytorch/pytorch/pull/49454)).
* Add 64bit indexing support for softmax ([#52713](https://github.com/pytorch/pytorch/pull/52713)).
* `nn.init._calculate_fan_in_and_fan_out`: Support usage with `__torch_function__` ([#53522](https://github.com/pytorch/pytorch/pull/53522)).
* `nn.Transformer` / `nn.MultiheadAttention`: Add `batch_first` argument ([#55285](https://github.com/pytorch/pytorch/pull/55285)).
* `nn.Transformer`: Add `layer_norm_eps` arg ([#54494](https://github.com/pytorch/pytorch/pull/54494)).
* `nn.AvgPool2d`: Add channels_last support on CPU ([#48918](https://github.com/pytorch/pytorch/pull/48918)).
* `clip_grad_norm_`: Add `error_if_nonfinite` flag ([#53843](https://github.com/pytorch/pytorch/pull/53843), [#55169](https://github.com/pytorch/pytorch/pull/55169)).
* `Module.train`: Raise nicer error when called with invalid modes ([#58247](https://github.com/pytorch/pytorch/pull/58247)).
* `nn.Linear`: Support 0 `in_features` ([#56505](https://github.com/pytorch/pytorch/pull/56505)).
* `nn.EmbeddingBag`: Support mix of int32 and int64 offsets/indices ([#55189](https://github.com/pytorch/pytorch/pull/55189)).
* `xnnpack::linear`: Handle 1D input ([#54986](https://github.com/pytorch/pytorch/pull/54986)).
* `nn.Module`: Add `allow_duplicate` flag to `named_modules()` ([#54812](https://github.com/pytorch/pytorch/pull/54812)).
* `nn.Module`: Add `to_empty()` function for moving to a device without copying storage ([#56610](https://github.com/pytorch/pytorch/pull/56610)).
* Make `pad_sequence` callable from C++ API ([#57868](https://github.com/pytorch/pytorch/pull/57868)).

### Dataloader

* Added `generate_state` for NumPy seeding ([#56797](https://github.com/pytorch/pytorch/pull/56797)).
* Modified construct_time_validation to argument_validation ([#55836](https://github.com/pytorch/pytorch/pull/55836)).
* Added mode to `LoadFilesFromDisk` ([#57056](https://github.com/pytorch/pytorch/pull/57056)).
* Added the ability to override *reduce_ex* function of `DataPipe` ([#52858](https://github.com/pytorch/pytorch/pull/52858)).
* Added lambda support to `MapIterDataPipe` ([#52856](https://github.com/pytorch/pytorch/pull/52856)).
* Added functional way of stacking DataPipes ([#52885](https://github.com/pytorch/pytorch/pull/52885)).

### C++ API

* Suppressed unsigned comparison warning ([#52653](https://github.com/pytorch/pytorch/pull/52653)).
* Fixed constexpr **host** warning ([#52702](https://github.com/pytorch/pytorch/pull/52702)).
* Introduced a fluent API to construct tensors from external data ([#54530](https://github.com/pytorch/pytorch/pull/54530)).

### AMD

* Allow PYTORCH_ROCM_ARCH in cpp_extension ([#54341](https://github.com/pytorch/pytorch/pull/54341)).
* Added support for `torch.half` dtype RNNs with MIOpen ([#52475](https://github.com/pytorch/pytorch/pull/52475)).
* Added support for the new `hiprtc` precompiler feature ([#54350](https://github.com/pytorch/pytorch/pull/54350)).
* Improved reliability of `hipfft` and `rocfft` detection for ROCm build ([#53408](https://github.com/pytorch/pytorch/pull/53408)).

### CUDA

* Improved warning message when old GPU is detected ([#56621](https://github.com/pytorch/pytorch/pull/56621))
* Made `torch.cuda.amp.GradScaler` scale updates in-place for better composability with graph capture ([#55562](https://github.com/pytorch/pytorch/pull/55562)).
* Add `USE_MAGMA` build flag ([#55994](https://github.com/pytorch/pytorch/pull/55994)).
* Change link order for BUILD_SPLIT_CUDA option ([#58437](https://github.com/pytorch/pytorch/pull/58437)).
* Improve CUDA-11.X binary builds ([#58459](https://l.workplace.com/l.php?u=https%3A%2F%2Fgithub.com%2Fpytorch%2Fpytorch%2Fpull%2F58459&h=AT1iY5lImKBK5tsZFPG9Ub57qOFMix4DslZFPlHNwT13OJnRq6Tvh_HehGQ-k4GF2bUDNhIQHBS578V8RQ-Sk2YYUv4Cys6KDIZPsunP7HzrwcYtfEZnPczt41cqT0KEIuvTSa1ZiOZ4SvvQV9F2xiYZ4cCJ7WIl2URyvg)).
* Move CUDA async warning to suffix ([#59467](https://github.com/pytorch/pytorch/pull/59467)).

### torch.fx

* Make `torch.fx.map_arg` require a callable ([#51907](https://github.com/pytorch/pytorch/pull/51907)).
* Generalize dict key check in `torch.fx.Tracer.create_arg` ([#51927](https://github.com/pytorch/pytorch/pull/51927)).
* Customize traceback for calls to symbolically-traced code ([#51648](https://github.com/pytorch/pytorch/pull/51648)).
* Allow `Transformer` to accept output result that is not Proxy ([#52473](https://github.com/pytorch/pytorch/pull/52473)).
* Make `TracerBase._find_user_frame` private ([#53654](https://github.com/pytorch/pytorch/pull/53654)).
* Improve buffer registration during `GraphModule` init ([#53444](https://github.com/pytorch/pytorch/pull/53444)).
* Garbage collect values in `Interpreter` ([#54726](https://github.com/pytorch/pytorch/pull/54726)).
* Improve placeholder matching in subgraph rewriter ([#54958](https://github.com/pytorch/pytorch/pull/54958)).
* Record `stride` on `Node` during `ShapeProp` pass ([#55108](https://github.com/pytorch/pytorch/pull/55108)).
* Record `memory_format` on `Node` during `ShapeProp` pass ([#55815](https://github.com/pytorch/pytorch/pull/55815)).
* Put tensor metadata into a `NamedTuple` in `ShapeProp` ([#55930](https://github.com/pytorch/pytorch/pull/55930)).
* Preserve node meta info in `split_module` ([#56212](https://github.com/pytorch/pytorch/pull/56212)).
* Make `shape_prop` handle targets with aggregate outputs ([#56221](https://github.com/pytorch/pytorch/pull/56221)).
* Make arg normalization a method on `Node` and not a pass (also augment tests to be exhaustive) ([#55992](https://github.com/pytorch/pytorch/pull/55992)).
* Allow for args to be left as args in NormalizeArgs ([#55995](https://github.com/pytorch/pytorch/pull/55995)).
* Maintain submodule references during subgraph rewriting ([#55463](https://github.com/pytorch/pytorch/pull/55463)).
* Changes in order to move `PythonKey` out of tree ([#57427](https://github.com/pytorch/pytorch/pull/57427)).
* Handle cases in `GraphDrawer` when shape, type or stride are not present ([#57845](https://github.com/pytorch/pytorch/pull/57845)).
* Handle the case when output consumes `get_attr` directly in `split_by_tags` ([#57844](https://github.com/pytorch/pytorch/pull/57844)).
* Let submodules be collected as `args/kwargs`  in symbolic tracing([#57840](https://github.com/pytorch/pytorch/pull/57840)).

### Profiler

* Expanded Kineto platform support ([#56323](https://github.com/pytorch/pytorch/pull/56323)).
* Added profiler fallback ([#57612](https://github.com/pytorch/pytorch/pull/57612)).
* Added CUDA event fallback ([#58133](https://github.com/pytorch/pytorch/pull/58133)).

### TorchScript

* Added a flag to enable CPU fusion in benchmarks ([#48612](https://github.com/pytorch/pytorch/pull/48612)).
* Updated fusion to handle loops that have the same bounds as expressions ([#55997](https://github.com/pytorch/pytorch/pull/55997)).
* Updated normalization transformation to be in-place ([#56158](https://github.com/pytorch/pytorch/pull/56158)).
* Added check to only lower float `conv2d`s ([#56289](https://github.com/pytorch/pytorch/pull/56289)).
* Added more python bindings for loopnest ([#56213](https://github.com/pytorch/pytorch/pull/56213)).
* Updated `fuseLoops` API to return bool flag and not throw any exceptions ([#56353](https://github.com/pytorch/pytorch/pull/56353)).
* Added `unroll` and `flatten` APIs which do not require return stmt pointer ([#56420](https://github.com/pytorch/pytorch/pull/56420)).
* Updated `Buf` on mutation instead of creating a new one ([#57513](https://github.com/pytorch/pytorch/pull/57513)).
* Updated `flatten` transformation to be in-place ([#56629](https://github.com/pytorch/pytorch/pull/56629)).
* Added missing python bindings for NNC Stmts ([#55570](https://github.com/pytorch/pytorch/pull/55570)).
* Allowed backend preprocessing to take place outside of the backend interface ([#51757](https://github.com/pytorch/pytorch/pull/51757))
* Added an error message for the case when `with` item is not an object ([#52335](https://github.com/pytorch/pytorch/pull/52335)).
* Enabled `ModuleList` non-literal indexing ([#53410](https://github.com/pytorch/pytorch/pull/53410)).
* Added recursive scripting for class type module attributes ([#55124](https://github.com/pytorch/pytorch/pull/55124)).
* Added support for `mypy` ignore annotation with particular rule specified ([#51675](https://github.com/pytorch/pytorch/pull/51675)).
* Added support for comparing two bool variables ([#51844](https://github.com/pytorch/pytorch/pull/51844)).
* Added MKLDNN GELU function ([#53615](https://github.com/pytorch/pytorch/pull/53615)).
* Added `hardtanh(0,6)` to the set of MKLDNN fusible ops for mobilenetv2 ([#56203](https://github.com/pytorch/pytorch/pull/56203)).
* Captured argument names for traced functions and modules ([#51775](https://github.com/pytorch/pytorch/pull/51775)).
* Improved `has_bf16_support` ([#57408](https://github.com/pytorch/pytorch/pull/57408)).
* Walk Python AST to check for unsupported attribute type annotations ([#51805](https://github.com/pytorch/pytorch/pull/51805)).
* Added `out` version for sum ([#52225](https://github.com/pytorch/pytorch/pull/52225))
* Added logic to trace `torch.nn.Linear` as `aten::linear` ([#51897](https://github.com/pytorch/pytorch/pull/51897)).
* Made `is_tracing` scriptable ([#49853](https://github.com/pytorch/pytorch/pull/49853)).
* Added support for builtin `sum` ([#52188](https://github.com/pytorch/pytorch/pull/52188)).
* Fused `clip_ranges` and `gather_ranges` ([#52461](https://github.com/pytorch/pytorch/pull/52461)).
* Added support for features from `to_backend` for the Lite Interpreter ([#52870](https://github.com/pytorch/pytorch/pull/52870)).
* Added a filter to remove mutation ([#51923](https://github.com/pytorch/pytorch/pull/51923)).
* Added logic functionalize ops which to be included in MKLDNN group ([#51924](https://github.com/pytorch/pytorch/pull/51924))
* Extended subgraph utils to cover merging a node following a subgraph ([#52513](https://github.com/pytorch/pytorch/pull/52513))
* Included max pool in fusion groups ([#52613](https://github.com/pytorch/pytorch/pull/52613)).
* Registered both TupleConstruct and ListConstruct as out variants ([#52684](https://github.com/pytorch/pytorch/pull/52684)).
* Added Alias analysis to Memory Management/Planning ([#50060](https://github.com/pytorch/pytorch/pull/50060)).
* Included max pool in fusion groups ([#52613](https://github.com/pytorch/pytorch/pull/52613)).
* Added property binding in TorchBind ([#50670](https://github.com/pytorch/pytorch/pull/50670)).
* Registered `pow` out variant ([#52454](https://github.com/pytorch/pytorch/pull/52454)).
* Made `torch.load()` aware of import path changes ([#53139](https://github.com/pytorch/pytorch/pull/53139)).
* Added `aten::to` copy out variant ([#52343](https://github.com/pytorch/pytorch/pull/52343)).
* Added more variants to `create_empty_from` ([#53333](https://github.com/pytorch/pytorch/pull/53333)).
* Added support for parsing Ellipsis in JIT frontend ([#53576](https://github.com/pytorch/pytorch/pull/53576)).
* Added a bool `is_available()` method to the backend contract ([#53068](https://github.com/pytorch/pytorch/pull/53068)).
* Added parallel support for the LLVM backend. ([#53243](https://github.com/pytorch/pytorch/pull/53243)) / Resubmit: Add parallel support for the LLVM backend. ([#54122](https://github.com/pytorch/pytorch/pull/54122)).
* Rewrote `functional.tensordot` to be TorchScript-able ([#53672](https://github.com/pytorch/pytorch/pull/53672)).
* Added python bindings for missing loop transformations in `LoopNest` ([#54355](https://github.com/pytorch/pytorch/pull/54355)).
* Added support for list insertion for mutation removal ([#54271](https://github.com/pytorch/pytorch/pull/54271)).
* Added support for  `torch.bfloat16` in the fuser ([#54571](https://github.com/pytorch/pytorch/pull/54571)).
* Added some functions for manipulating MKLDNN tensors to TORCH_API ([#56954](https://github.com/pytorch/pytorch/pull/56954)).
* Merged CUDA Streams and Events ([#53902](https://github.com/pytorch/pytorch/pull/53902)).
* Added python bindings for `TensorExprKernel` ([#54450](https://github.com/pytorch/pytorch/pull/54450)).
* Added support for dtype-specific tensor subclasses (e.g. LongTensor) ([#54817](https://github.com/pytorch/pytorch/pull/54817)).
* Added support for tuple `add` operator ([#52292](https://github.com/pytorch/pytorch/pull/52292)).
* Disambiguated error message for working with not fully refined tuple types ([#55745](https://github.com/pytorch/pytorch/pull/55745)).
* Allowed unpacking tuple and assigning unpacked values to SELECT-type expressions ([#55268](https://github.com/pytorch/pytorch/pull/55268)).
* Made NoneType `annotation_str` emit `NoneType` instead of `None` ([#54746](https://github.com/pytorch/pytorch/pull/54746)).
* Added CUDA device synchronization support in JIT ([#55469](https://github.com/pytorch/pytorch/pull/55469)).
* Added `optimize_graph_output_memory` flag ([#55811](https://github.com/pytorch/pytorch/pull/55811)).
* Added support for refinement for `torch.jit.Future` ([#56148](https://github.com/pytorch/pytorch/pull/56148)).
* Added implicit conversion from null tensor to `NoneType `([#55823](https://github.com/pytorch/pytorch/pull/55823)).
* Added `aten::matmul`s to TE fuser ([#54605](https://github.com/pytorch/pytorch/pull/54605)).
* Put explicit error message on class attribute accesses ([#55723](https://github.com/pytorch/pytorch/pull/55723)).
* Added support for constant tensors in tensorexpr kernel ([#56319](https://github.com/pytorch/pytorch/pull/56319)).
* Added native support for `aten::getitem` ([#55310](https://github.com/pytorch/pytorch/pull/55310)).
* Added stricter check for function schemas with varargs ([#56509](https://github.com/pytorch/pytorch/pull/56509)).
* Added graceful failure handling of DataPtr extraction in CUDAFuture ([#56511](https://github.com/pytorch/pytorch/pull/56511)).
* Enabled forward/backward compatibility in TS mobile ([#56079](https://github.com/pytorch/pytorch/pull/56079)).
* Added binding for `aten::clamp_min_out` ([#56635](https://github.com/pytorch/pytorch/pull/56635)), `aten::argmin_out` ([#56638](https://github.com/pytorch/pytorch/pull/56638)), and `aten::norm_out` ([#56636](https://github.com/pytorch/pytorch/pull/56636)).
* Enhanced error message for `Future.setErrorIfNeeded` ([#56631](https://github.com/pytorch/pytorch/pull/56631)).
* Added type inference support for `nn.Module `methods using PDT ([#57165](https://github.com/pytorch/pytorch/pull/57165)).
* Disabled conv-add-relu fusion for cuDNN7 when model uses `torch.float16` ([#56579](https://github.com/pytorch/pytorch/pull/56579)).
* Enabled conv-add-relu fusion as a part of frozen graph optimization ([#56580](https://github.com/pytorch/pytorch/pull/56580)).
* Reduced inline autodiff threshold to enable the capture of smaller fusions ([#57062](https://github.com/pytorch/pytorch/pull/57062)).
* Added static runtime support for `aten::matmul` ([#57291](https://github.com/pytorch/pytorch/pull/57291)).
* Added `device()` method to `c10::Event` ([#57293](https://github.com/pytorch/pytorch/pull/57293)).
* Added support for normalization of `is` op ([#57862](https://github.com/pytorch/pytorch/pull/57862)).
* Enabled `cat` without conditionals iff CPU ([#58026](https://github.com/pytorch/pytorch/pull/58026)).
* Added `LowerSimpleTuples` for freeze tuples ([#57915](https://github.com/pytorch/pytorch/pull/57915)).
* Added support for striding for list slicing ([#49352](https://github.com/pytorch/pytorch/pull/49352)).
* Wrapped `torch::deploy` API functions in safe rethrow macros ([#58192](https://github.com/pytorch/pytorch/pull/58192)).
* Added binding for `aten::div_out` ([#56653](https://github.com/pytorch/pytorch/pull/56653))
* Added binding for `aten::sub_out` ([#56656](https://github.com/pytorch/pytorch/pull/56656)).
* Supported `clamp.Tensor `([#58191](https://github.com/pytorch/pytorch/pull/58191)).
* Added an out version for `aten::repeat` ([#57683](https://github.com/pytorch/pytorch/pull/57683)).
* Added default arguments to CUDA stream and events ([#53025](https://github.com/pytorch/pytorch/pull/53025)).
* Added support for linear in MKLDNN fusion ([#51484](https://github.com/pytorch/pytorch/pull/51484)).
* Handled MKLDNN broadcasting in MKLDNN fuser ([#51736](https://github.com/pytorch/pytorch/pull/51736)).
* Added 0-dim support for binary MKLDNN ops ([#51921](https://github.com/pytorch/pytorch/pull/51921)).
* Added OneDNN relu backward and reshape backward ([#49455](https://github.com/pytorch/pytorch/pull/49455)).
* Added OneDNN batch_norm backward ([#50460](https://github.com/pytorch/pytorch/pull/50460)).
* Added support for `hardshrink` ([#57749](https://github.com/pytorch/pytorch/pull/57749)).
* Added non mutator bundled inputs method ([#58408](https://github.com/pytorch/pytorch/pull/58408)).
* Added support to compare devices ([#53045](https://github.com/pytorch/pytorch/pull/53045)).
* Added support for `memory_arg` in `aten::clone` ([#58100](https://github.com/pytorch/pytorch/pull/58100)).
* Implemented `aten::cat` without conditionals ([#53128](https://github.com/pytorch/pytorch/pull/53128)).
* Added external function bindings ([#53420](https://github.com/pytorch/pytorch/pull/53420)).
* Added out variant of `sigrid_transforms_torch_bind` and `ListUnpack` ([#54761](https://github.com/pytorch/pytorch/pull/54761)).

### torch.package

* Added a reliable method for determining if a file is part of Python’s standard library  ([#51694](https://github.com/pytorch/pytorch/pull/51694)).
* Made package code more composable with other parts of PyTorch (package GraphModule, load non-code files from package) ([#51674](https://github.com/pytorch/pytorch/pull/51674), [#51976](https://github.com/pytorch/pytorch/pull/51976)).
* Improved debugging facilities (allow_empty flag, zip file viewer, deny instruction, dependency tracing, query if object is from a package)  ([#53232,](https://github.com/pytorch/pytorch/pull/53232)[#53233](https://github.com/pytorch/pytorch/pull/53233), [#52176](https://github.com/pytorch/pytorch/pull/52176), [#55167](https://github.com/pytorch/pytorch/pull/55167), [#56190](https://github.com/pytorch/pytorch/pull/56190), [#56238](https://github.com/pytorch/pytorch/pull/56238), [#56729](https://github.com/pytorch/pytorch/pull/56729)).
* Allow save_module to accept module as arg ([#55996](https://github.com/pytorch/pytorch/pull/55996)).
* Follow dependencies created by `__import__` calls ([#55153](https://github.com/pytorch/pytorch/pull/55153)).
* Added hooks to exporters’ mock and extern calls to take action when a module is matched ([#58000](https://github.com/pytorch/pytorch/pull/58000))
* Turn the default behavior of packaging into an ‘intern’ action so that it can be ordered with repeat to mock, extern, and deny actions ([#57341](https://github.com/pytorch/pytorch/pull/57341)).

### Quantization

* Added support for keeping output quantized for list and dict ([#56391](https://github.com/pytorch/pytorch/pull/56391)).
* Added `torch.float16` and `torch.float64` support to `fake_quantize_per_channel` ([#56894](https://github.com/pytorch/pytorch/pull/56894)).
* Support preserving attributes in deepcopy of observed/quantized graphmodule ([#56550](https://github.com/pytorch/pytorch/pull/56550)).
* Added support for packed params in state_dict ([#51639](https://github.com/pytorch/pytorch/pull/51639)).
* Added support for fusing `Conv3d + BatchNorm3d + ReLU` operations ([#50003](https://github.com/pytorch/pytorch/pull/50003)).
* Change back to `multiple_outputs_gpu_kernel` for learnable fake per-channel quantization ([#52017](https://github.com/pytorch/pytorch/pull/52017)).
* Added `torch.float16` and `torch.float32` support to `fake_quantize_per_tensor` ([#52612](https://github.com/pytorch/pytorch/pull/52612)).
* Support batched embeddings for 8 Bit embedding bag quantization ([#55343](https://github.com/pytorch/pytorch/pull/55343)).
* Expose nbins and ratio for `quantized::embedding_bag_4bit_prepack` ([#50398](https://github.com/pytorch/pytorch/pull/50398)).

### Mobile

* Removed caching of inflated bundled inputs ([#55181](https://github.com/pytorch/pytorch/pull/55181)).
* Improved exception reporting for Lite interpreter ([#54284](https://github.com/pytorch/pytorch/pull/54284), [#55062](https://github.com/pytorch/pytorch/pull/55062), [#55252](https://github.com/pytorch/pytorch/pull/55252)).
* Improved forward/backward compatibility in Lite interpreter when adding new optional arguments to ops ([#56845](https://github.com/pytorch/pytorch/pull/56845)).
* Added model size to logged metadata when loading a Lite interpreter model ([#53578](https://github.com/pytorch/pytorch/pull/53578)).
* Benchmarking binary speed_benchmark_torch now supports Lite interpreter ([#55402](https://github.com/pytorch/pytorch/pull/55402)).

### Distributed

`torch.distributed.Store`

* Update `compare_set` for other Store implementations to be the same as `TCPStore`. ([#57175](https://github.com/pytorch/pytorch/pull/57175))
* `torch.distributed.Store`: Expose C++ `compare_set` API to python. ([#57191](https://github.com/pytorch/pytorch/pull/57191))
* `torch.distributed.Store`: Add `timeout`, `host`, `port` to TCPStore’s python API as accessors. ([#52784](https://github.com/pytorch/pytorch/pull/52784))
* Allow `world_size` and `is_master` to be optional when constructing TCPStore. ([#51809](https://github.com/pytorch/pytorch/pull/51809))
* Add `wait_for_worker` param to `TCPStore`’s Python API([#52888](https://github.com/pytorch/pytorch/pull/52888))

`torch.distributed.rpc`

* Allow `RRef` to be created with a specified set of CUDA devices ([#57085](https://github.com/pytorch/pytorch/pull/57085))
* Correctness fixes for CUDA support in RPC framework ([#54024](https://github.com/pytorch/pytorch/pull/54024), )
* Refactor RPC agent to use `Store` to collect and verify name ([#53209](https://github.com/pytorch/pytorch/pull/53209), [#53202](https://github.com/pytorch/pytorch/pull/53202))

`DistributedDataParallel`

* Make unused parameter search show up in profiler output ([#57376](https://github.com/pytorch/pytorch/pull/57376))
* Update DDP communication hooks to divide by world size before all_reduce to avoid overflow ([#57410](https://github.com/pytorch/pytorch/pull/57410))
* Stabilize `torch.distributed.GradBucket` interface for gradient compression ([#53010](https://github.com/pytorch/pytorch/pull/53010), [#53098](https://github.com/pytorch/pytorch/pull/53098), [#53102](https://github.com/pytorch/pytorch/pull/53102), [#53009](https://github.com/pytorch/pytorch/pull/53009), [#53099](https://github.com/pytorch/pytorch/pull/53099))
* Skip CPU to GPU input copy if input is already on the right device. ([#55624](https://github.com/pytorch/pytorch/pull/55624))
* Record forward pass of `DistributedDataParallel` and `DataParallel` in profiler.([#55578](https://github.com/pytorch/pytorch/pull/55578))
*  Make `orthogonalization_epsilon` flag configurable in `torch.distributed.algorithms.ddp_comm_hooks.powerSGD_hook.PowerSGDState` ([#55738](https://github.com/pytorch/pytorch/pull/55738))
* Set default value of `start_powerSGD_iter` to 1K iterations in 
    `torch.distributed.algorithms.ddp_comm_hooks.powerSGD_hook. `([#55272](https://github.com/pytorch/pytorch/pull/55272))
* Add a minimum compression rate threshold parameter for `torch.distributed.algorithms.ddp_comm_hooks.powerSGD_hook`   ([#52541](https://github.com/pytorch/pytorch/pull/52541))
* Report compression rate for batched PowerSGD hook ([#55103](https://github.com/pytorch/pytorch/pull/55103))
* Enable gradient compression hook testing on ROCm ([#52403](https://github.com/pytorch/pytorch/pull/52403))
* Enhance warning for unused parameters in `DistributedDataParallel`. ([#52385](https://github.com/pytorch/pytorch/pull/52385))
* Enhance error messages when crashing with unused parameters in `DistributedDataParallel`. ([#52391](https://github.com/pytorch/pytorch/pull/52391))

`torch.distributed`

* Add rank information on NCCL communicator abort ([#57974](https://github.com/pytorch/pytorch/pull/57974))
* Enhance exception logging in NCCL ([#54557](https://github.com/pytorch/pytorch/pull/54557), [#54558](https://github.com/pytorch/pytorch/pull/54558), [#54117](https://github.com/pytorch/pytorch/pull/54117))

`torch.distributed.nn.RemoteModule`

* Create a separate remote module template when moving CPU tensors to a cuda device is not enabled ([#57413](https://github.com/pytorch/pytorch/pull/57413))
* Allow passing `RemoteModule` as an argument over RPC ([#57695](https://github.com/pytorch/pytorch/pull/57695), [#58345](https://github.com/pytorch/pytorch/pull/58345))
* Support async instantiation of RemoteModule ([#58052](https://github.com/pytorch/pytorch/pull/58052))
* Place inputs on the appropriate devices in `RemoteModule` ([#56943](https://github.com/pytorch/pytorch/pull/56943))

`torch.futures.Future`

* Enable `torch.futures.Future` to be created with CUDA support ([#56517](https://github.com/pytorch/pytorch/pull/56517)) 
* `torch.futures`: Improve error propagation when using `then` API ([#54475](https://github.com/pytorch/pytorch/pull/54475))

`torch.nn.SyncBatchNorm`

* Migrate `apex.parallel.SyncBatchNorm` `channels_last` to PyTorch implementation ([#46906](https://github.com/pytorch/pytorch/pull/46906))
* Fix `SyncBatchNorm`’s forward pass to handle optional weight ([#54568](https://github.com/pytorch/pytorch/pull/54568))

`torch.distributed.pipeline`

* `torch.distributed.pipeline`: Merge pipeline partitions that are on the same device. ([#55973](https://github.com/pytorch/pytorch/pull/55973))

Added new `torch.distributed.elastic `module that upstreams `pytorch/elastic`

* Rename `torch.distributed.elastic_launch` to `torch.distributed.run` ([#56831](https://github.com/pytorch/pytorch/pull/56831))
* make process failure init error non-fatal ([#56739](https://github.com/pytorch/pytorch/pull/56739))
* Reorder type definitions in dynamic_rendezvous.py ([#56534](https://github.com/pytorch/pytorch/pull/56534))
* Revise the rendezvous handler registry logic. ([#55466](https://github.com/pytorch/pytorch/pull/55466))
* Set error code in reply file when child process is terminated by signals. (f665a7f8a1)
* Make sure torchelastic mp wait for queue to be drained before finishing the process ([#55412](https://github.com/pytorch/pytorch/pull/55412))
* Revise the rendezvous exception types. ([#54803](https://github.com/pytorch/pytorch/pull/54803))
* Expose a `stderr` parameter in `EtcdServer`. ([#54805](https://github.com/pytorch/pytorch/pull/54805))
* Improve the implementation of the utility functions and add their unit tests. ([#54804](https://github.com/pytorch/pytorch/pull/54804))
* Improve the implementation of `RendezvousParameters` and add its unit tests. ([#54807](https://github.com/pytorch/pytorch/pull/54807))

`torch.distributed.optim.ZeroRedundancyOptimizer`

* Add an option for buckets to be views of tensors and consolidate public interface ([#52987](https://github.com/pytorch/pytorch/pull/52987))
* Make state dict for ZeroRedundancyOptimizer world size independent ([#52960](https://github.com/pytorch/pytorch/pull/52960))

Combine backtrace print into one string to avoid interleaving ([#56961](https://github.com/pytorch/pytorch/pull/56961)).
Raise exception rather than crash if GLOO_DEVICE_TRANSPORT is set to unknown value ([#58518](https://github.com/pytorch/pytorch/issues/58518)).

### ONNX

* Updated fuseLogSoftmaxNllLoss function to handle autocasting ([#51729](https://github.com/pytorch/pytorch/pull/51729)) ([#52349](https://github.com/pytorch/pytorch/pull/52349)).
* Added support for sequence of tensor mutations in blocks ([#51577](https://github.com/pytorch/pytorch/pull/51577)) ([#52347](https://github.com/pytorch/pytorch/pull/52347)).
* Updated LayerNorm symbolic to handle autocasting ([#52199](https://github.com/pytorch/pytorch/pull/52199)) ([#52350](https://github.com/pytorch/pytorch/pull/52350)).
* Restored fast path in `OnnxifiOp::adjustOutputBatchSize` ([#52498](https://github.com/pytorch/pytorch/pull/52498)).
* Improved index_put symbolic to handle singular Bool updates ([#53690](https://github.com/pytorch/pytorch/pull/53690)) ([#54863](https://github.com/pytorch/pytorch/pull/54863)).
* Replaced decomposeLinear pre process pass with a symbolic ([#53077](https://github.com/pytorch/pytorch/pull/53077)) ([#54866](https://github.com/pytorch/pytorch/pull/54866)).
* Improved assign input shape for tuple inputs & primitive type inputs ([#54112](https://github.com/pytorch/pytorch/pull/54112)) ([#56164](https://github.com/pytorch/pytorch/pull/56164)).
* Updated repeat_interleave symbolic ([#54312](https://github.com/pytorch/pytorch/pull/54312)) ([#56165](https://github.com/pytorch/pytorch/pull/56165)).
* Enabled `word_language_model` GRU and LSTM scripting ([#54310](https://github.com/pytorch/pytorch/pull/54310)) ([#56170](https://github.com/pytorch/pytorch/pull/56170)).
* Added standardOps match more input type in ORT ([#53813](https://github.com/pytorch/pytorch/pull/53813)) ([#56172](https://github.com/pytorch/pytorch/pull/56172)).
* Redesigned in-place conversion ([#55033](https://github.com/pytorch/pytorch/pull/55033)) ([#56173](https://github.com/pytorch/pytorch/pull/56173)).
* Handled PackedParams inputs for _propagate_and_assign_input_shapes ([#56449](https://github.com/pytorch/pytorch/pull/56449)) ([#57079](https://github.com/pytorch/pytorch/pull/57079)).
* Added a warning for the case when *len* is used to calculate tensor shape ([#55151](https://github.com/pytorch/pytorch/pull/55151)) ([#57595](https://github.com/pytorch/pytorch/pull/57595)).
* Added special post processing for `onnx::Cast` and `onnx::ConstantOfShape` shape type inference ([#55962](https://github.com/pytorch/pytorch/pull/55962)) ([#57597](https://github.com/pytorch/pytorch/pull/57597)).
* Handled NoneType in Assign Output Shapes ([#54623](https://github.com/pytorch/pytorch/pull/54623)) ([#57602](https://github.com/pytorch/pytorch/pull/57602)).
* ListUnpack on dynamic tensor list ([#56592](https://github.com/pytorch/pytorch/pull/56592)) ([#57603](https://github.com/pytorch/pytorch/pull/57603)).
* Handled mixed mask, index input for index_put ([#57604](https://github.com/pytorch/pytorch/pull/57604)).
* Handled incorrect format for example_outputs ([#55802](https://github.com/pytorch/pytorch/pull/55802)) ([#57829](https://github.com/pytorch/pytorch/pull/57829)).
* Enabled several script unit tests using new jit passes ([#51722](https://github.com/pytorch/pytorch/pull/51722)) ([#53309](https://github.com/pytorch/pytorch/pull/53309)).

### Vulkan

* Enabled broadcasting for arithmetic ops (add, sub, mul, and div) ([#52842](https://github.com/pytorch/pytorch/pull/52842)).
* Reduced size of compiled shaders by using the `-Os` flag when calling `glslc` ([#57199](https://github.com/pytorch/pytorch/pull/57199)).
* The vulkan optimization JIT pass now adds an `optimized_for_vulkan` attribute to the model ([#56414](https://github.com/pytorch/pytorch/pull/56414)).

### Benchmark

* Quality of life improvements to Timer ([#53294](https://github.com/pytorch/pytorch/pull/53294))
* Add repeats to Timer.collect_callgrind(...) ([#54484](https://github.com/pytorch/pytorch/pull/54484))

### Misc

* Auto-detect ccache to speed up developer builds ([#49389](https://github.com/pytorch/pytorch/pull/49389)).
* Catch and ignore tracebacks for compilation errors ([#55986](https://github.com/pytorch/pytorch/pull/55986)).
* Register DefaultBackend implementations for functional/inplace structured operators ([#53037](https://github.com/pytorch/pytorch/pull/53037)).
* Improved support for oneDNN on AArch64 when building from src ([#55913](https://github.com/pytorch/pytorch/pull/55913)).


# Bug fixes

### Python API

* Updated `torch.lerp`  to make `weights` tensor broadcast-able ([#52319](https://github.com/pytorch/pytorch/pull/52319)).
* Fixed print for negative torch.int8 tensors on ARM64 ([#52616](https://github.com/pytorch/pytorch/pull/52616)).
* Fixed type annotation for `as_tuple` to clearly determine what `torch.nonzero` will resolve to ([#51635](https://github.com/pytorch/pytorch/pull/51635)).
* Fixed `torch.logcumsumexp` to correctly handle infs and nans ([#52947](https://github.com/pytorch/pytorch/pull/52947)).
* Fixed `torch.topk` for k=0 on CUDA by skipping the kernel launch in this case ([#58086](https://github.com/pytorch/pytorch/pull/58086)).
* Fixed a bug for optimizers to have the hyper parameters be still defined when all parameters have no grad ([#52944](https://github.com/pytorch/pytorch/pull/52944)).
* Fixed type promotion issue for `torch.pow` ([#54085](https://github.com/pytorch/pytorch/pull/54085)).
* Fixed `torch.min()` and `torch.max()` to work on a non-empty dimension for tensors with 0 elements ([#52565](https://github.com/pytorch/pytorch/pull/52565)).
* Fixed the upper bound computation for `torch.randperm` ([#56967](https://github.com/pytorch/pytorch/pull/56967)).
* Allowed `std=0` in `torch.normal`, and added checks to consistently error out if `std<0` ([#51317](https://github.com/pytorch/pytorch/pull/51317))
* Fixed  `torch.index_fill` to output 0-dim tensor for a 0-dim input tensor ([#52209](https://github.com/pytorch/pytorch/pull/52209)).
* Fixed mul_() to correctly work for Mkldnn tensors ([#51758](https://github.com/pytorch/pytorch/pull/51758)).
* Fixed temp file/bind race condition in torch_shm_manager for `torch.multiprocessing` ([#57309](https://github.com/pytorch/pytorch/pull/57309)).
* Fixed tempfile address binding in torch_shm_manager to be destructed correctly for `torch.multiprocessing` ([#57566](https://github.com/pytorch/pytorch/pull/57566)).
* Fixed `torch.multinomial` to never select an element with 0 weight for `torch.half` (already works correctly for other datatypes) ([#53480](https://github.com/pytorch/pytorch/pull/53480)).
* Fixed a bug in `assertRaises` `NotImplemented` handling when no exception is thrown ([#54126](https://github.com/pytorch/pytorch/pull/54126)).
* Fixed override for `__iter__` ([#54702](https://github.com/pytorch/pytorch/pull/54702)).
* Fixed segmentation fault for `torch.floor_divide` when compiling on ARM64 ([#55608](https://github.com/pytorch/pytorch/pull/55608)).
* Fixed `torch.digamma`’s inconsistency with SciPy’s digamma ([#56689](https://github.com/pytorch/pytorch/pull/56689)).
* Fixed `torch.cat` to return correct result for non-contiguous tensors ([#57177](https://github.com/pytorch/pytorch/pull/57177)).
* Fixed distributions for `torch.distributions.log_prob` which don't properly honor `validate_args=False` ([#53600](https://github.com/pytorch/pytorch/pull/53600)).
* De-prioritized `Dimname` and `DimnameList` in python overload resolution ([#51350](https://github.com/pytorch/pytorch/pull/51350)).
* Fixed the handling of scalar and zero dimensional inputs as well to `torch.take()` and `torch.Tensor.put_` on both CPU and CUDA ([#53356](https://github.com/pytorch/pytorch/pull/53356)).
* Fixed a bug to not rebuild extensions for every import ([#56015](https://github.com/pytorch/pytorch/pull/56015)).
* Fixed error message for `torch.as_strided` ([#53198](https://github.com/pytorch/pytorch/pull/53198)).
* Added correct handling for tensor allocation for large tensors when using `torch.resize` on CUDA ([#52672](https://github.com/pytorch/pytorch/pull/52672)).
* Fixed an illegal memory access that could happen when computing the inverse of a batch of matrices on CUDA ([#53064](https://github.com/pytorch/pytorch/pull/53064)).
* Fixed a bug where `torch.sparse.addmm` would compute the wrong results for CUDA inputs when beta was not zero or one ([#56160](https://github.com/pytorch/pytorch/pull/56160)).
* Fixed a bug where `torch.sparse.sparse_coo_tensor`’s gradient could be calculated incorrectly ([#50361](https://github.com/pytorch/pytorch/pull/50361)).
* `pow`: Fixed a bug caused for mixed cpu/cuda input tensors ([#53669](https://github.com/pytorch/pytorch/pull/53669)).
* `sub`: Fixed a `sub.Scalar` bug ([#53679](https://github.com/pytorch/pytorch/pull/53679)).
* Fixed `torch.unique` for discontiguous inputs ([#59003](https://github.com/pytorch/pytorch/pull/59003)).
* Fixed `torch.randperm` on CUDA ([#59352](https://github.com/pytorch/pytorch/pull/59352)).
* Fix `torch.reciprocal` for `torch.float32` on ARMv8 ([#59361](https://github.com/pytorch/pytorch/pull/59361)).
* Disable overloading of std::max & std::min for inputs of different types, which could cause accuracy loss ([#55638](https://github.com/pytorch/pytorch/pull/55638))

### Complex Numbers

* Added custom implementation for `sqrt` and `acos` to be used if `libc++` is used to reduce numerical error for edge cases. ([#52018](https://github.com/pytorch/pytorch/pull/52018), [#54820](https://github.com/pytorch/pytorch/pull/54820), [#52287](https://github.com/pytorch/pytorch/pull/52287)).

### Autograd

* Fixed
    * `torch.autograd.gradgradcheck` when outputs are independent of the inputs ([#58049](https://github.com/pytorch/pytorch/pull/58049)).
    * `torch.utils.checkpoint` to behave properly when an error happens during forward ([#51746](https://github.com/pytorch/pytorch/pull/51746)).
    * autograd’s graph discovery when output is a leaf that requires gradients ([#51940](https://github.com/pytorch/pytorch/pull/51940)).
    * some cases where `torch.autograd.gradcheck` did not return the correct value when `raise_exception=False`  ([#53916](https://github.com/pytorch/pytorch/pull/53916)) .
    * thread local state not being properly propagated for some operations during the backward pass ([#56174](https://github.com/pytorch/pytorch/pull/56174)).
    * `torch.index_fill_` formula to support duplicate indices ([#57101](https://github.com/pytorch/pytorch/pull/57101)).
    * derivative of `torch.sinc` around `x=0` ([#56763](https://github.com/pytorch/pytorch/pull/56763), [#56986](https://github.com/pytorch/pytorch/pull/56986)).
    * `torch.cdist` backward formula to correctly support broadcasting ([#56605](https://github.com/pytorch/pytorch/pull/56605)) and empty inputs ([#56606](https://github.com/pytorch/pytorch/pull/56606)).
    * view creation metadata for functions that return multiple views in `no_grad` or inference mode. ([#57842](https://github.com/pytorch/pytorch/pull/57842)).
    * `autograd.functional.*` functions to work in no_grad mode ([#47543](https://github.com/pytorch/pytorch/pull/47543)).
    * rare deadlocks on exit due to autograd worker threads ([#53170](https://github.com/pytorch/pytorch/pull/53170)).

### torch.nn

* `nn.AdaptiveAveragePooling`: Fix crash for integral inputs ([#51443](https://github.com/pytorch/pytorch/pull/51443)).
* `F.normalize`: Fix to make it properly scriptable ([#51909](https://github.com/pytorch/pytorch/pull/51909)).
* `nn.parallel.scatter_gather.gather`: Fix to handle `NamedTuple`s and moving output to CPU ([#51104](https://github.com/pytorch/pytorch/pull/51104)).
* `fractional_max_pool{2/3}d` : Fix segfaults for incorrect `kernel_size` and `output_size` ([#51626](https://github.com/pytorch/pytorch/pull/51626)).
* `nn.CosineEmbeddingLoss`: Validate target has correct shape ([#53110](https://github.com/pytorch/pytorch/pull/53110)).
* Fix multiprocessing serialization for integer parameters on CUDA ([#56529](https://github.com/pytorch/pytorch/pull/56529)).
* `nn.Softplus`: Fix backwards computation by comparing `input` against `beta * threshold` ([#56484](https://github.com/pytorch/pytorch/pull/56484)).
* `addmm_`: Add check to disallow resizing the input tensor for the in-place variation on CPU ([#56452](https://github.com/pytorch/pytorch/pull/56452)).
* `nn.InstanceNorm*d`: Fix to perform correct input size check ([#56659](https://github.com/pytorch/pytorch/pull/56659)).
* `nn.CTCLoss`: Fix backward pass regression on cuDNN ([#56639](https://github.com/pytorch/pytorch/pull/56639)).
* `nn.ConvTranspose*d`: Fix regression that broke padding with a list of values ([#54911](https://github.com/pytorch/pytorch/pull/54911)).
* `F.max_pool3d`: Fix illegal memory access for large inputs on CUDA by doing multiplication in `int64` ([#52828](https://github.com/pytorch/pytorch/pull/52828)).
* `F.embedding`: Support `__torch_function__` ([#54478](https://github.com/pytorch/pytorch/pull/54478)).
* `nn.ChannelShuffle`: Remove `NamedTensor` warnings ([#55911](https://github.com/pytorch/pytorch/pull/55911)).
* `mkldnn_linear`: Fix incorrect results for non-contiguous inputs ([#51713](https://github.com/pytorch/pytorch/pull/51713)).
* `nn.ModuleList` / `nn.ModuleDict`: Raise `NotImplementedError` for `forward()` ([#48785](https://github.com/pytorch/pytorch/pull/48785)).
* Change `maybe_resize_storage_cpu` `new_size` arg to unsigned ([#52671](https://github.com/pytorch/pytorch/pull/52671)).
* `nn.LSTM`: Fix regression that broke loading older serialized modules ([#57558](https://github.com/pytorch/pytorch/pull/57558)).
* `F.reflection_pad2d`: Fix CUDA launch error ([#56451](https://github.com/pytorch/pytorch/pull/56451)).
* Fix wrong detection of depthwise convolution on neon ([#55794](https://github.com/pytorch/pytorch/pull/55794)).
* Re-enable fast winograd convolution on IOS ([#56021](https://github.com/pytorch/pytorch/pull/56021)).
* `gaussian_nll_loss`: Fix incorrect `reduction=‘none’` behavior ([#56469](https://github.com/pytorch/pytorch/pull/56469)).
* Fix misaligned access #56325 ([#56403](https://github.com/pytorch/pytorch/pull/56403)).
* Use native CTC loss for target length 256 ([#53557](https://github.com/pytorch/pytorch/pull/53557)).
* `register_full_backward_hook`: Fix crash when first argument doesn't require a gradient ([#57945](https://github.com/pytorch/pytorch/pull/57945)).
* Remove asserts of Tensor type and ignore mypy checks to support `__torch_function__` usage ([#57458](https://github.com/pytorch/pytorch/pull/57458)).
* Handle stride > 1 with im2col in CUDA thnn conv2d ([#54080](https://github.com/pytorch/pytorch/pull/54080)).
* Add device id to ConvolutionParams ([#50892](https://github.com/pytorch/pytorch/pull/50892)).
* Enabling OneDNN for group convolution ([#54890](https://github.com/pytorch/pytorch/pull/54890)).
* `nn.AdaptiveAveragePooling3d`: Add `AccumulateType` for CUDA ([#53607](https://github.com/pytorch/pytorch/pull/53607)).
* Do not use depthwise3x3 conv in grad mode for ARM ([#56889](https://github.com/pytorch/pytorch/pull/56889)).
* Fix type annotations for `state_dict()` override ([#55704](https://github.com/pytorch/pytorch/pull/55704)).
* Pass contiguous weight to NNPACK convolution ([#56569](https://github.com/pytorch/pytorch/pull/56569)).
* `nn.EmbeddingBag`: Mark backward as non-deterministic for max mode rather than all reducing modes ([#55574](https://github.com/pytorch/pytorch/pull/55574)).
* `nn.EmbeddingBag`: Initialize `bag_size` output with zeros to make it deterministic ([#56661](https://github.com/pytorch/pytorch/pull/56661)).
* `nn.EmbeddingBag`: Support the empty bag case on CPU ([#57446](https://github.com/pytorch/pytorch/pull/57446)).
* Fix `nn.MHA` + `quantized` scriptability ([#58727](https://github.com/pytorch/pytorch/pull/58727)).
* Fixes cuDNN performance on A100 ([#58287](https://github.com/pytorch/pytorch/pull/58287), [#59721](https://github.com/pytorch/pytorch/pull/59721), [#59744](https://github.com/pytorch/pytorch/pull/59744), [#59802](https://github.com/pytorch/pytorch/pull/59802)).

### Dataloader

* Fixed type hints of the callable DataLoader arguments ([#52924](https://github.com/pytorch/pytorch/pull/52924)).
* Added a keyword arg to meta and support `abc` for typing ([#58450](https://github.com/pytorch/pytorch/pull/58450)).
* Fixed a bug to use `generator` instead of `self.generator` in the `RandomSampler` ([#52956](https://github.com/pytorch/pytorch/pull/52956)).

### C++ API

* Fixed the lifetime of `PyTensorType` ([#51649](https://github.com/pytorch/pytorch/pull/51649)).
* Fixed linker failure with ambiguous namespaces ([#45736](https://github.com/pytorch/pytorch/pull/45736)).
* Fix Scalar output formatting ([#53229](https://github.com/pytorch/pytorch/pull/53229))
* Fix printing of optional string arguments in schemas ([#55196](https://github.com/pytorch/pytorch/pull/55196))

### AMD

* Fixed `hipfft` transform type error ([#53411](https://github.com/pytorch/pytorch/pull/53411)).
* Load only hipfft for ROCm > 4.1 ([#54349](https://github.com/pytorch/pytorch/pull/54349)).

### CUDA

* Added `torch.scatter_add` to `torch.cuda.amp` promote list ([#52133](https://github.com/pytorch/pytorch/pull/52133)).
* Fixed segfault in distributed process group due to IPC ([#53080](https://github.com/pytorch/pytorch/pull/53080)).
* Fixed multinomial CUDA misalignment and non-deterministic behavior ([#55364](https://github.com/pytorch/pytorch/pull/55364)).
* Replaced raw cudaMalloc in `torch.sparse` code ([#57083](https://github.com/pytorch/pytorch/pull/57083)).
* [CUDA graphs] Added proper sync after replay ([#57556](https://github.com/pytorch/pytorch/pull/57556)).
* Fixed NVRTC versioning for CUDA 11.X (X>=3), CUDA 12 and later ([#57204](https://github.com/pytorch/pytorch/pull/57204)).
* Fixed a correctness issue of CUDA channels-last `nn.SyncBatchNorm` ([#57077](https://github.com/pytorch/pytorch/pull/57077)).
* Fixed CUDA caching allocator when trying to allocate ~2^64 memory ([#57571](https://github.com/pytorch/pytorch/pull/57571)).
* Fixed raw_deleter() bug with PYTORCH_NO_CUDA_MEMORY_CACHING=1 ([#54775](https://github.com/pytorch/pytorch/pull/54775)).
* Fixed undefined symbol for CUDA 11.1 Windows ([#52506](https://github.com/pytorch/pytorch/pull/52506)).
* Automatically set BUILD_SPLIT_CUDA for cpp extensions ([#52503](https://github.com/pytorch/pytorch/pull/52503)).
* Adds grid_sampler to the list of operations that can autocast `torch.float32` ([#58679](https://github.com/pytorch/pytorch/pull/58679)).

### Dispatcher

* Fix boxing/unboxing for `Scalar` bool values ([#53228](https://github.com/pytorch/pytorch/pull/53228))
* Fix inaccurate dispatch table for `fill_` ([#53611](https://github.com/pytorch/pytorch/pull/53611))
* Fix inaccurate dispatch tables ([#54127](https://github.com/pytorch/pytorch/pull/54127))
* Fix issue with dispatch key: `AutogradXPU` ([#56336](https://github.com/pytorch/pytorch/pull/56336))
* Modify `DispatchKeyExtractor` to also work for optional Tensors ([#58283](https://github.com/pytorch/pytorch/pull/58283))
* Extract dispatch keys from optional Tensors (unboxed) ([#58296](https://github.com/pytorch/pytorch/pull/58296))

### torch.fx

* Preserve leaf modules in `Transformer` ([#51998](https://github.com/pytorch/pytorch/pull/51998)).
* Fix tuple type annotations in FX codebase ([#52010](https://github.com/pytorch/pytorch/pull/52010)).
* Fix type correctness on `GraphModule.graph` ([#54305](https://github.com/pytorch/pytorch/pull/54305)).
* Remove `forward` from `forward.__globals__` to facilitate retracing ([#54011](https://github.com/pytorch/pytorch/pull/54011)).
* Fix `ScriptMethod` dispatch on `__torch_function__` ([#56103](https://github.com/pytorch/pytorch/pull/56103)).
* Fix `type_matches` for `Optional[List[int]]` arguments to make `NormalizeArgs` more permissive ([#56790](https://github.com/pytorch/pytorch/pull/56790)).
* Fix `NormalizeArgs` issues with lists of tensors ([#57004](https://github.com/pytorch/pytorch/pull/57004)).
* Changed parametric type error in `NormalizeArgs` to a warning ([#57183](https://github.com/pytorch/pytorch/pull/57183)).
* Make `NormalizeArgs` not save output node in the `node_map` ([#58058](https://github.com/pytorch/pytorch/pull/58058)).

### Profiler

* Fixed intermittent CUDA activity flush issue (https://github.com/pytorch/kineto/pull/95).
* Handled empty trace ([#58013](https://github.com/pytorch/pytorch/pull/58013)).
* Added cuda synchronization points ([#56651](https://github.com/pytorch/pytorch/pull/56651)).
* Removed usage of onEachDevice from legacy profiler ([#54125](https://github.com/pytorch/pytorch/pull/54125)).
* Fixed double printing of FLOPs ([#56974](https://github.com/pytorch/pytorch/pull/56974)).

### TorchScript

* Fixed `jit.trace` mishandling of InterfaceType ([#53052](https://github.com/pytorch/pytorch/pull/53052)).
* Made `reshape`/`flatten` deterministic ([#54353](https://github.com/pytorch/pytorch/pull/54353)).
* Added logic to use `is_buffer` in `BufferPolicy::valid` ([#49588](https://github.com/pytorch/pytorch/pull/49588)).
* Updated NNC to sanitize input names ([#52786](https://github.com/pytorch/pytorch/pull/52786)).
* Handled ExternalCalls in LoadStore analysis and Inliner ([#52628](https://github.com/pytorch/pytorch/pull/52628)).
* Fixed output restriding of size-1 dimensions ([#58256](https://github.com/pytorch/pytorch/pull/58256)).
* Handled non literal constant bounds in Unroll ([#53029](https://github.com/pytorch/pytorch/pull/53029)).
* Fixed a case where inlining wouldn't work because dim-size was 1 ([#53254](https://github.com/pytorch/pytorch/pull/53254)).
* Removed cached argv from LLVMCodeGen to fix race condition ([#54286](https://github.com/pytorch/pytorch/pull/54286)).
* Lowered scalar constants as doubles/longs ([#54824](https://github.com/pytorch/pytorch/pull/54824)).
* Added a check to not try to vectorize kernels that use float16 ([#55970](https://github.com/pytorch/pytorch/pull/55970)).
* Added a check to not fuse `torch.float16` on CPU ([#56119](https://github.com/pytorch/pytorch/pull/56119)).
* Fixed `float->bool` conversion on CPU ([#57798](https://github.com/pytorch/pytorch/pull/57798)).
* Fixed handling of the arguments of `aten::to` ([#58028](https://github.com/pytorch/pytorch/pull/58028)).
* Don’t error on 0-dim in convolution ([#51922](https://github.com/pytorch/pytorch/pull/51922)).
* Allow `__exit__` to have a return value ([#52336](https://github.com/pytorch/pytorch/pull/52336)).
* Added metacompile of ternary if ([#51789](https://github.com/pytorch/pytorch/pull/51789)).
* Keep alive graph when creating iterators from it ([#51951](https://github.com/pytorch/pytorch/pull/51951)).
* Fixed return value of `IValue::to` for Tensor/String ([#51463](https://github.com/pytorch/pytorch/pull/51463)).
* Added function to check for memory leak ([#52342](https://github.com/pytorch/pytorch/pull/52342)).
* Ignore user annotated ignored attributes ([#52367](https://github.com/pytorch/pytorch/pull/52367)).
* Fixed `jit.trace` mishandling of InterfaceType ([#53052](https://github.com/pytorch/pytorch/pull/53052)).
* Fixed tracing support for TorchBind ([#52884](https://github.com/pytorch/pytorch/pull/52884)).
* Use correct warning type for tracer warnings ([#53460](https://github.com/pytorch/pytorch/pull/53460)).
* Removed the assumption that `forward` exists in freeze_module ([#52918](https://github.com/pytorch/pytorch/pull/52918)).
* Removed notion of "level" from `Module::dump_to_str` ([#52539](https://github.com/pytorch/pytorch/pull/52539)).
* Made `IValue::toTensor()` inline-able ([#53213](https://github.com/pytorch/pytorch/pull/53213)).
* Consider `normal_` as a special operation in the remove mutation pass ([#52175](https://github.com/pytorch/pytorch/pull/52175)).
* Updated `set_stream` API to change the device ([#53741](https://github.com/pytorch/pytorch/pull/53741)).
* Only run `ReplaceWithCopy` pass when `enable_out_variant` is true ([#54111](https://github.com/pytorch/pytorch/pull/54111)).
* Disable dfusion group that is not supported by XPU device ([#54239](https://github.com/pytorch/pytorch/pull/54239)).
* Don’t require same-sized `src`/`dest` in `reshape_copy` ([#54467](https://github.com/pytorch/pytorch/pull/54467)).
* Fixed `TupleType.annotation_str` to conform to `typing` module syntax for empty tuple type ([#54641](https://github.com/pytorch/pytorch/pull/54641)).
* Made NoneType `annotation_str` emit `NoneType` instead of `None` ([#54642](https://github.com/pytorch/pytorch/pull/54642)).
* Made sure the copy version of the op exists in `ReplaceWithCopy` ([#55337](https://github.com/pytorch/pytorch/pull/55337)).
* Included `conv3d` in `conv-add-relu` fusion ([#54772](https://github.com/pytorch/pytorch/pull/54772)).
* Added `cond-add-relu` matching pattern to cover in-place ops ([#55458](https://github.com/pytorch/pytorch/pull/55458)).
* Fixed `TupleType.annotation_str` to conform to `typing` module syntax for empty tuple type ([#54745](https://github.com/pytorch/pytorch/pull/54745)).
* Fixed `Optional[Tensor]` type in autodiff ([#55565](https://github.com/pytorch/pytorch/pull/55565)).
* Raise TypeErrors when `IValue::getSubValues` fails ([#56510](https://github.com/pytorch/pytorch/pull/56510)).
* Fixed num args for `to_copy` ([#56441](https://github.com/pytorch/pytorch/pull/56441))
* Fixed error in JIT CUDA on ROCm ([#55243](https://github.com/pytorch/pytorch/pull/55243)).
* Fixed a bug in `emitUse` to drop all values that are marked as drop ([#56652](https://github.com/pytorch/pytorch/pull/56652)).
* Fixed default dtype for `randperm` and `triu`/`tril_indices` inside TorchScript ([#57105](https://github.com/pytorch/pytorch/pull/57105)).
* Don't allow create() on singleton types ([#56807](https://github.com/pytorch/pytorch/pull/56807)).
* Fix GIL mutithreading issue exposed by `torch::jit::toIValue()` ([#57688](https://github.com/pytorch/pytorch/pull/57688)).
* Fold `NaiveSyncBatchNorm` when folding batch norm ([#57823](https://github.com/pytorch/pytorch/pull/57823)).
* Fix UB in `LoopNest::distribute` ([#57883](https://github.com/pytorch/pytorch/pull/57883)).
* Fix a condition when we use a native depthwise `conv2d` lowering ([#57906](https://github.com/pytorch/pytorch/pull/57906)).
* Ensure `torch.save()` has deterministic output ([#57536](https://github.com/pytorch/pytorch/pull/57536))
* Fixed `hasattr` support type ([#57950](https://github.com/pytorch/pytorch/pull/57950))
* Return nullptr if the number of input args doesn't match ([#58018](https://github.com/pytorch/pytorch/pull/58018)).
* Added fix for missing ops `aten::sorted.str` ([#58339](https://github.com/pytorch/pytorch/pull/58339)).
* Fixed deadlock in `Future` due to lock inversion with GIL ([#58382](https://github.com/pytorch/pytorch/pull/58382)).
* Added logic to prevent lock inversions with GIL in `Future` ([#58391](https://github.com/pytorch/pytorch/pull/58391)).
* Fixed `MKLDNN_add` in-place behavior ([#51687](https://github.com/pytorch/pytorch/pull/51687)).
* Use MKLDNN copy for `copy_ when` self and src are MKLDNN layout ([#54248](https://github.com/pytorch/pytorch/pull/54248)) .
* Fixed default to align with documentation in `fuser.py` ([#53457](https://github.com/pytorch/pytorch/pull/53457)).
* Fixed upcoming changes that are part of ROCm 4.2 and affect PyTorch JIT ([#57400](https://github.com/pytorch/pytorch/pull/57400)).
* Fix for improper mobile and torch.package serialization ([#59642](https://github.com/pytorch/pytorch/pull/59642)).

### torch.package

* Add cpython as a dependency for torch_python_obj ([#56740](https://github.com/pytorch/pytorch/pull/56740)).
* Catch exceptions where dependency resolution gets invalid imports ([#58573](https://github.com/pytorch/pytorch/pull/58573)).
* Simplifications to broken dependency handling ([#58572](https://github.com/pytorch/pytorch/pull/58572)).

### Quantization

* Fixed conv packed param serialization in `state_dict` ([#52787](https://github.com/pytorch/pytorch/pull/52787)).
* Fixed `torch.float16` dynamic quant for functional linear ([#52369](https://github.com/pytorch/pytorch/pull/52369)).
* Fixed prepacking for `F.conv1d` ([#55311](https://github.com/pytorch/pytorch/pull/55311)).
* MHA tensor assignment fix ([#53031](https://github.com/pytorch/pytorch/pull/53031)).
* Fixed `conv` transpose with `qconfig == None` ([#52844](https://github.com/pytorch/pytorch/pull/52844)).
* Quant norm layers: move scale + zp to buffers ([#52861](https://github.com/pytorch/pytorch/pull/52861)).
* Handled the case when observed node has no users ([#53210](https://github.com/pytorch/pytorch/pull/53210)).
* Only insert observers for fixed qparam ops ([#53330](https://github.com/pytorch/pytorch/pull/53330)).
* Fixed a condition check for `CopyNode` ([#53585](https://github.com/pytorch/pytorch/pull/53585)).
* Fix for `x.ndim` followed by `sub` ([#53120](https://github.com/pytorch/pytorch/pull/53120)).
* Fixed using size of quant layer in `torch._assert` ([#53187](https://github.com/pytorch/pytorch/pull/53187)).
* Fixed fx quant for `quant_layer -> stack -> sum` ([#53196](https://github.com/pytorch/pytorch/pull/53196)).
* Fixed `deepcopy` on quantized `ConvNd` ([#56154](https://github.com/pytorch/pytorch/pull/56154))
* Fixed `getitem` for unmatched nodes ([#57173](https://github.com/pytorch/pytorch/pull/57173)).
* Made quantizeable MHA work with `torch.jit.script` ([#57774](https://github.com/pytorch/pytorch/pull/57774)).
* Fixed `quantize_per_tensor` on CUDA ([#57703](https://github.com/pytorch/pytorch/pull/57703)).
* Fixed a bug to handle bias in rowwise quantization of FC ([#58022](https://github.com/pytorch/pytorch/pull/58022)).
* Skipped inserting observer for boolean Tensors ([#57375](https://github.com/pytorch/pytorch/pull/57375)).
* Fixed `torch.float16` reference patterns for linear ([#55727](https://github.com/pytorch/pytorch/pull/55727)).
* FX Quant:
    * Fixed edge case with copynode after user function ([#55710](https://github.com/pytorch/pytorch/pull/55710)).
    * Fixed subtle bug in BinaryOpQuantizeHanlder logic in matching ([#56294](https://github.com/pytorch/pytorch/pull/56294)).
    * Fixed bug with fusion patterns and disabling quantization ([#54654](https://github.com/pytorch/pytorch/pull/54654)).
* Fixed overflow issue in quantized instance_norm/layer_norm/group_norm ([#54872](https://github.com/pytorch/pytorch/pull/54872)).
* Fixed zero_point rounding for _fake_quantize_learnable_per_channel_affine ([#52290](https://github.com/pytorch/pytorch/pull/52290)).
* Bug fix to update requantization and zp parameters of input ([#52797](https://github.com/pytorch/pytorch/pull/52797)).
* Fix embedding bag bug accessing unaligned memory ([#53300](https://github.com/pytorch/pytorch/pull/53300)).
* Fix out variant for 4bit embedding bag ([#55096](https://github.com/pytorch/pytorch/pull/55096)).
* Avoid tensor refcount bumps on embedding bag ([#55023](https://github.com/pytorch/pytorch/pull/55023)).

### Mobile

* Fixed some bugs in the implementation of various functions on iOS GPU:
    * `max_pool_2d` when padding is used ([#52431](https://github.com/pytorch/pytorch/pull/52431)).
    * `softmax` ([#54519](https://github.com/pytorch/pytorch/pull/54519)).
    * binary element-wise ops to handle inputs with different number of dimensions ([#58262](https://github.com/pytorch/pytorch/pull/58262)).
* Removed duplication of constant tensors in model when using Lite interpreter ([#58182](https://github.com/pytorch/pytorch/pull/58182), [#56002](https://github.com/pytorch/pytorch/pull/56002)).
* Banned mutating operators in mobile GPU models ([#56070](https://github.com/pytorch/pytorch/pull/56070)).
* Use lite interpreter as default and bump model version ([#58630](https://github.com/pytorch/pytorch/pull/58630))

### Distributed

`torch.distributed.Store`

* Fix flag specifying whether there is more data for `TCPStore` delete key ([#53886](https://github.com/pytorch/pytorch/pull/53886))
* Properly enforce timeout for `PrefixStore`. ([#53928](https://github.com/pytorch/pytorch/pull/53928))
* Fix `TCPStore` `wait` hang when key is previously set ([#53860](https://github.com/pytorch/pytorch/pull/53860))
* Properly order `TCPStore`’s `compare_set` parameters in Python API ([#52696](https://github.com/pytorch/pytorch/pull/52696))
* Fix resource leak bug in TCPStore constructor ([#52860](https://github.com/pytorch/pytorch/pull/52860))

`torch.distributed.rpc`

* Several fixes for CUDA support in the RPC framework ([#57926](https://github.com/pytorch/pytorch/pull/57926), [#57432](https://github.com/pytorch/pytorch/pull/57432), [#57394](https://github.com/pytorch/pytorch/pull/57394), [#57443](https://github.com/pytorch/pytorch/pull/57443), [#57487](https://github.com/pytorch/pytorch/pull/57487), [#58384](https://github.com/pytorch/pytorch/pull/58384), [#51820](https://github.com/pytorch/pytorch/pull/51820), [#57792](https://github.com/pytorch/pytorch/pull/57792), [#56895](https://github.com/pytorch/pytorch/pull/56895), [#54932](https://github.com/pytorch/pytorch/pull/54932))
* Fix possible reference cycle by passing reference to parent future in RPC callbacks ([#57635](https://github.com/pytorch/pytorch/pull/57635))
* Fix RPC `get_worker_info` for rank 0 ([#52804](https://github.com/pytorch/pytorch/pull/52804))
* Fix crash when TensorPipe agent tries to double-set errors. ([#52837](https://github.com/pytorch/pytorch/pull/52837))

`torch.distributed`

* Fix path handling on Windows during rendezvous process ([#57000](https://github.com/pytorch/pytorch/pull/57000))
* Fix and re-enable `ProcessGroupMPITest` ([#56709](https://github.com/pytorch/pytorch/pull/56709))

`DistributedDataParallel`

*  Correct the usage of min_compression_rate in gradient compression communication hooks ([#52979](https://github.com/pytorch/pytorch/pull/52979))
* Fix mapping of parameter to parameter names when certain parameters don’t require gradient ([#57771](https://github.com/pytorch/pytorch/pull/57771))
* Skip rebuild buckets in `DistributedDataParallel` when running under `no_grad` mode. ([#54159](https://github.com/pytorch/pytorch/pull/54159))
* Fix a race condition in `DistributedDataParallel` when all parameters are used but running with `find_unused_parameters=True`. ([#53160](https://github.com/pytorch/pytorch/pull/53160))
* In `DistributedDataParallel`, pass in `process_group` argument into `dist.get_rank` calls ([#53793](https://github.com/pytorch/pytorch/pull/53793))
* Fix `DistributedDataParallel`’s process for verifying model consistency during initialization. ([#52887](https://github.com/pytorch/pytorch/pull/52887))

`torch.distributed`

* Check vector boundaries in `torch::cuda::scatter` ([#53057](https://github.com/pytorch/pytorch/pull/53057))
* Release GIL before destructing ProcessGroup classes ([#56381](https://github.com/pytorch/pytorch/pull/56381))

`torch.distributed.pipeline`

* Fix hang in `pipeline` destructor by removing `join_workers` ([#53433](https://github.com/pytorch/pytorch/pull/53433))

`torch.distributed.elastic`

* Resolve bug around incorrect rendezvous handler resolution ([#56386](https://github.com/pytorch/pytorch/pull/56386))

`torch.nn.SyncBatchNorm`

* Ensure `SyncBatchNorm` behaves like a regular `BatchNorm` layer in eval mode. ([#56982](https://github.com/pytorch/pytorch/pull/56982))

`torch.distributed.optim.ZeroRedundancyOptimizer`

* Typing fixes([#53165](https://github.com/pytorch/pytorch/pull/53165))

Fix monitored_barrier with wait_all_ranks ([#58702](https://github.com/pytorch/pytorch/pull/58702)).

### ONNX

* Removed the last Cast in pow symbolic_opset9 ([#52646](https://github.com/pytorch/pytorch/pull/52646)) ([#53305](https://github.com/pytorch/pytorch/pull/53305)).
* Fixed export of `copy_` operator ([#53046](https://github.com/pytorch/pytorch/pull/53046)) ([#53310](https://github.com/pytorch/pytorch/pull/53310)) ([#51938](https://github.com/pytorch/pytorch/pull/51938)) ([#54870](https://github.com/pytorch/pytorch/pull/54870)).
* Fixed export of embedding with `padding_idx` ([#53053](https://github.com/pytorch/pytorch/pull/53053)) ([#53530](https://github.com/pytorch/pytorch/pull/53530)).
* Fixed onnx warning message ([#54371](https://github.com/pytorch/pytorch/pull/54371)).
* Improved error message during Glow ONNXIFI ([#58069](https://github.com/pytorch/pytorch/pull/58069)).
* Fixed if output shape mismatch error & graph input directly used as output ([#53219](https://github.com/pytorch/pytorch/pull/53219)) ([#54865](https://github.com/pytorch/pytorch/pull/54865)).
* Fixed ComputeShapeFromReshape when `input_shape_size < reshape_size` ([#56171](https://github.com/pytorch/pytorch/pull/56171)).
* Fixed -Wrange-loop-construct in onnx_exporter.cc ([#56759](https://github.com/pytorch/pytorch/pull/56759)).
* Print `onnxifi` failed status code in readable format ([#53648](https://github.com/pytorch/pytorch/pull/53648)).

### Vulkan

* Fixed kernel registration errors in Vulkan test and benchmark binaries by adding `nonVarTypeModeGuard` ([#52535](https://github.com/pytorch/pytorch/pull/52535)).
* Fixed the `glslc` path in CMake for desktop builds ([#56507](https://github.com/pytorch/pytorch/pull/56507)).
* Fixed build failures caused by `warnings-treated-as-error` for Linux builds. ([#52781](https://github.com/pytorch/pytorch/pull/52781)).
* Remove constant duplication for Vulkan optimize_for_mobile ([#59276](https://github.com/pytorch/pytorch/pull/59276)).

### Benchmark

* Fix timer overflow on small, fast snippets ([#55200](https://github.com/pytorch/pytorch/pull/55200))

### Misc

* [memory format] Fixed channels last bug in upsample kernels to now correctly pass `memory_format` information from the input to the output tensors ([#53535](https://github.com/pytorch/pytorch/pull/53535)).
* [memory format] Fixed silent correctness bug for CUDA upsample kernels to correctly handle `torch.channels_last` contiguous tensors ([#54744](https://github.com/pytorch/pytorch/pull/54744)).
* Workaround intermittent gcc-7.5 ICE in cpp tests ([#57016](https://github.com/pytorch/pytorch/pull/57016)).
* Improve build quality on Windows ([#52729](https://github.com/pytorch/pytorch/pull/52729), [#53562](https://github.com/pytorch/pytorch/pull/53562), [#54132](https://github.com/pytorch/pytorch/pull/54132), [#55275](https://github.com/pytorch/pytorch/pull/55275)).
* Search for static OpenBLAS compiled with OpenMP ([#59428](https://github.com/pytorch/pytorch/pull/59428)).


# Performance

### Python API

* Optimized memory usage for `out=` version of `torch`.`logsumexp` ([#51239](https://github.com/pytorch/pytorch/pull/51239)).
* Added vectorization for `torch.floor_divide` ([#55380](https://github.com/pytorch/pytorch/pull/55380)).
* Reimplemented `torch.flip()` using advanced indexing ([#56713](https://github.com/pytorch/pytorch/pull/56713)).
* Improved performance for `torch.take()` and `torch.Tensor.put_` on both CPU and CUDA ([#53356](https://github.com/pytorch/pytorch/pull/53356))
* Generic performance improvement for operations performed on non-contiguous 2-dimensional tensors ([#53613](https://github.com/pytorch/pytorch/pull/53613)).
* Added vectorization for `torch.copysign` on CPU ([#51792](https://github.com/pytorch/pytorch/pull/51792)).
* Improved performance for bilinear interpolation on CPU ([#51653](https://github.com/pytorch/pytorch/pull/51653)).
* Improved performance for backward computations on `torch.cumsum` and `torch.cumprod` on both CPU and CUDA ([#53711](https://github.com/pytorch/pytorch/pull/53711)).
* Improved performance for `torch.Tensor.copy_`  when performing copies between small tensors of `torch.float` and `torch.half` data types ([#53800](https://github.com/pytorch/pytorch/pull/53800)).
* Enabled vectorization for `torch.Tensor.copy_` and `torch.cat` for BFloat16 tensors ([#54671](https://github.com/pytorch/pytorch/pull/54671), [#54674](https://github.com/pytorch/pytorch/pull/54674)).
* Added a fast path for a common case for `torch.addmm` on CUDA ([#55026](https://github.com/pytorch/pytorch/pull/55026)).
* In collaboration with NVIDIA, the CUDA performance of many linear algebra operations has been improved by increasing use of the cuSOLVER and cuBLAS libraries
    * Added cuBLAS support for `torch.triangular_solve` ([#53147](https://github.com/pytorch/pytorch/pull/53147)) and batched `torch.geqrf` ([#56253](https://github.com/pytorch/pytorch/pull/56253)).
    * Added cuSOLVER support for `torch.linalg.eigh/eigvalsh` ([#53040](https://github.com/pytorch/pytorch/pull/53040)), `torch.cholesky_solve` ([#54315](https://github.com/pytorch/pytorch/pull/54315)), `torch.cholesky_inverse` ([#54676](https://github.com/pytorch/pytorch/pull/54676)), and `torch.linalg.q`r ([#56256](https://github.com/pytorch/pytorch/pull/56256)).
    * Added cuBLAS and cuSOLVER support for `torch.linalg.lstsq` ([#57317](https://github.com/pytorch/pytorch/pull/57317)).
* Improved performance for `torch.nonzero` ([#58468](https://github.com/pytorch/pytorch/pull/58468)).
* Removed device check from a few indexing methods ([#58800](https://github.com/pytorch/pytorch/pull/58800)).

### Complex Numbers

* Added a faster path for `torch.is_complex()` by skipping unnecessary  dispatch ([#50054](https://github.com/pytorch/pytorch/pull/50054)).

### Autograd

* Sped up autograd’s graph discovery algorithm by skipping some nodes using sequence number ([#52180](https://github.com/pytorch/pytorch/pull/52180), [#52057](https://github.com/pytorch/pytorch/pull/52057)).
* Added a new fast gradcheck ([#54480](https://github.com/pytorch/pytorch/pull/54480)).

### torch.nn

* `Module.forward`: Add fast path for the case of no hooks ([#52576](https://github.com/pytorch/pytorch/pull/52576)).
* Fix `mkldnn` heuristic for multithreaded convolution ([#52909](https://github.com/pytorch/pytorch/pull/52909)).
* `linear`: Remove one refcount bump ([#54936](https://github.com/pytorch/pytorch/pull/54936)).
* Improve `native_batch_norm_backward` performance on CUDA ([#58240](https://github.com/pytorch/pytorch/pull/58240)).
* `nll_loss`: Use cascade summation on CPU ([#55841](https://github.com/pytorch/pytorch/pull/55841)).
* `nn.BatchNorm1d`: Improve training performance on CPU ([#57033](https://github.com/pytorch/pytorch/pull/57033)).
* Simplify convolution double backward gradInput formulas ([#54840](https://github.com/pytorch/pytorch/pull/54840)).
* Move RNN cell size check to cpp ([#51964](https://github.com/pytorch/pytorch/pull/51964)).
* Remove syncs in `one_hot` ([#57902](https://github.com/pytorch/pytorch/pull/57902)).
* Enable and enhance bf16 threshold ([#54384](https://github.com/pytorch/pytorch/pull/54384)).
* `nn.Conv3d`: Enable `channels_last_3d` for cuDNN ([#48430](https://github.com/pytorch/pytorch/pull/48430)).
* Increase token count threshold for calling thrust sort in embedding backward ([#49913](https://github.com/pytorch/pytorch/pull/49913)).
* CPU convolution benchmark harness for some popular models ([#56455](https://github.com/pytorch/pytorch/pull/56455)).
* Improved performance for `torch.nn.BatchNorm1d` on both CPU and CUDA ([#57033](https://github.com/pytorch/pytorch/pull/57033), [#57786](https://github.com/pytorch/pytorch/pull/57786)).
* Added optimized generic interpolation for `torch.nn.functional.{upsample_nearest`, `upsample_bicubic}` and speed up for channels first and last cases ([#54500](https://github.com/pytorch/pytorch/pull/54500)).
* Added shape documentation for CosineEmbeddingLoss ([#58403](https://github.com/pytorch/pytorch/pull/58403)).

### C++ API

* Fixed nest openmp performance bug in `thnn_conv2d` ([#52577](https://github.com/pytorch/pytorch/pull/52577)).
* Added c10::MaybeOwned and Tensor::expect_contiguous ([#53317](https://github.com/pytorch/pytorch/pull/53317))
* Added DimVector variant of infer_size ([#54882](https://github.com/pytorch/pytorch/pull/54882))
* Added logic to use `DimVector` for inputs to `as_strided `that don't grow dim ([#55016](https://github.com/pytorch/pytorch/pull/55016)).
* Reduce ref-counting by borrowing in/out Tensors in TensorIterator ([#55690](https://github.com/pytorch/pytorch/pull/55690)).
* Reduce ref-counting by migrating add operators to borrow Tensors in TensorIteratorBase ([#55691](https://github.com/pytorch/pytorch/pull/55691)).
* Reduce ref-counting by migrating copy_ operators to borrow input/output Tensors ([#56031](https://github.com/pytorch/pytorch/pull/56031)).
* Added logic to use `expect_contiguous` in `layer_norm` ([#58067](https://github.com/pytorch/pytorch/pull/58067)).

### CUDA

* Construct only necessary elements in OffsetCalculator ([#55107](https://github.com/pytorch/pytorch/pull/55107)).
* Migrated `torch.index_put` to use cub instead of thrust ([#55693](https://github.com/pytorch/pytorch/pull/55693)).
* Added cuSOLVER `potrf` and `potrfBatched` to the backend of `torch.cholesky_decomposition` ([#53104](https://github.com/pytorch/pytorch/pull/53104)).
* Implemented `torch.sort` with cub::DeviceSegmentedRadixSort ([#56821](https://github.com/pytorch/pytorch/pull/56821)).
* Added cuSOLVER path for `torch.geqrf` ([#56252](https://github.com/pytorch/pytorch/pull/56252)).
* Enabled cuSOLVER `torch.potrf` batched for Cholesky decomposition when CUDA >= 11.3 ([#57788](https://github.com/pytorch/pytorch/pull/57788)).
* Fewer CUDA sync in unique by using cub instead of thrust ([#57323](https://github.com/pytorch/pytorch/pull/57323)).
* Removed sync for `randperm` on small tensors ([#54113](https://github.com/pytorch/pytorch/pull/54113)).
* Simplify convolution double backward gradInput formulas ([#54840](https://github.com/pytorch/pytorch/pull/54840)).

### Composability

* We’ve landed lots of performance optimizations for 1.9, both large and small. See individual PRs for details:
    * Inline `tensor.device()` ([#50848](https://github.com/pytorch/pytorch/pull/50848))
    * Skip a second call to `shouldUseRecordFunction` for BackendSelect ops ([#50891](https://github.com/pytorch/pytorch/pull/50891))
    * Re-order `TensorImpl` fields to save a word ([#50920](https://github.com/pytorch/pytorch/pull/50920))
    * Devirtualize `TensorImpl::storage()` ([#51050](https://github.com/pytorch/pytorch/pull/51050))
    * Reduce template expansion in `call_functor_with_args_from_stack` (build time) ([#51313](https://github.com/pytorch/pytorch/pull/51313))
    * Eliminate `WrapFunctionIntoRuntimeFunctor `use in CppFunction constructors ([#51315](https://github.com/pytorch/pytorch/pull/51315))
    * Remove `reference_cast` in `make_boxed_from_unboxed_functor` (build time) ([#51319](https://github.com/pytorch/pytorch/pull/51319))
    * Debug-gate `static_assert` in `KernelFunction::makeFromUnboxedFunctor` (build time) ([#51367](https://github.com/pytorch/pytorch/pull/51367))
    * Use real `if constexpr` behind macro in hot template (build time) ([#51368](https://github.com/pytorch/pytorch/pull/51368), [#52420](https://github.com/pytorch/pytorch/pull/52420))
    * Outline `DispatchStub::get_call_ptr()` ([#51908](https://github.com/pytorch/pytorch/pull/51908))
    * Use `torchCheckFail` in `TORCH_INTERNAL_ASSERT` ([#52086](https://github.com/pytorch/pytorch/pull/52086))
    * Add `Storage::set_data_ptr_noswap` and use where possible ([#52244](https://github.com/pytorch/pytorch/pull/52244))
    * Make shared empty string static instead of thread_local ([#52220](https://github.com/pytorch/pytorch/pull/52220))
    * Avoid `std::string` in `TORCH_CHECK` when possible ([#52221](https://github.com/pytorch/pytorch/pull/52221))
    * Make `c10::str(const char*)` return `const char*` ([#52222](https://github.com/pytorch/pytorch/pull/52222))
    * Sync `TORCH_INTERNAL_ASSERT` optimizations with `TORCH_CHECK` ([#52226](https://github.com/pytorch/pytorch/pull/52226))
    * Save a single add instruction in the dispatcher ([#52543](https://github.com/pytorch/pytorch/pull/52543))
    * Inline `TensorIteratorConfig` setters ([#52661](https://github.com/pytorch/pytorch/pull/52661))
    * Use `DimVector` for sizes and strides in `view` ([#53001](https://github.com/pytorch/pytorch/pull/53001))
    * Avoid TLS in `has_names` ([#53003](https://github.com/pytorch/pytorch/pull/53003))
    * Don't inline `Dispatcher::call` on mobile (binary size) ([#53197](https://github.com/pytorch/pytorch/pull/53197))
    * Skip dispatch for `is_floating_point` ([#53242](https://github.com/pytorch/pytorch/pull/53242))
    * Move non-template part of `TensorImpl::Resize` to cpp (binary size, build time) ([#53388](https://github.com/pytorch/pytorch/pull/53388))
    * Don't copy vector arguments to `Tensor::Resize` ([#53389](https://github.com/pytorch/pytorch/pull/53389))
    * Skip dispatch trip for CPU in `resize_` ([#53575](https://github.com/pytorch/pytorch/pull/53575))
    * Pass `Scalar` by reference ([#53583](https://github.com/pytorch/pytorch/pull/53583))
    * Don't use static for template declarations in headers (binary size) ([#53602](https://github.com/pytorch/pytorch/pull/53602))
    * Boxing logic forwards arguments to stack ([#53624](https://github.com/pytorch/pytorch/pull/53624))
    * `Speed up Tensor::data_ptr by using static item size (`[`#53723`](https://github.com/pytorch/pytorch/pull/53723)`)`
    * `Skip dispatch for is_signed (`[`#53847`](https://github.com/pytorch/pytorch/pull/53847)`)`
    * Allow inlining of more Tensor methods ([#53905](https://github.com/pytorch/pytorch/pull/53905))
    * `Tensor::register_hook`: Avoid wrapping hook in two levels of `std::function` ([#53917](https://github.com/pytorch/pytorch/pull/53917))
    * Take advantage of string literals in `TORCH_WARN` ([#54032](https://github.com/pytorch/pytorch/pull/54032))
    * Inline `Tensor` keyset-checking methods & similar getters ([#54806](https://github.com/pytorch/pytorch/pull/54806))
    * `TensorIterator::output` returns const reference ([#54811](https://github.com/pytorch/pytorch/pull/54811))
    * Avoid refcount bump in `TensorArg` ([#54934](https://github.com/pytorch/pytorch/pull/54934))
    * Move `Tensor::has_names` inline ([#54965](https://github.com/pytorch/pytorch/pull/54965))
    * `OperandInfo` ctor should take rvalue reference ([#54972](https://github.com/pytorch/pytorch/pull/54972))
    * Don't bother with `SmallVector` in `TensorMaker` ([#55125](https://github.com/pytorch/pytorch/pull/55125))
    * Eliminate device guard in generic dispatch key kernel wrappers ([#55131](https://github.com/pytorch/pytorch/pull/55131))
    * Move logic to skip a redispatch directly inside of `resize_output` ([#55162](https://github.com/pytorch/pytorch/pull/55162))
    * Use `infer_size_dimvector` in `ExpandUtils` ([#55180](https://github.com/pytorch/pytorch/pull/55180))
    * Don't create intermediate Tensor for `at::result_type` w/Scalar ([#55232](https://github.com/pytorch/pytorch/pull/55232))
    * Use `sizes()[x]` instead of `size(x)` in `addr` ([#55247](https://github.com/pytorch/pytorch/pull/55247))
    * Add & use `inferExpandGeometry_dimvector` ([#55316](https://github.com/pytorch/pytorch/pull/55316))
    * Mark borrowed case as `C10_LIKELY` in `MaybeOwned` ([#55553](https://github.com/pytorch/pytorch/pull/55553))
    * Avoid double indirection in `MaybeOwned`'s borrowed state ([#55685](https://github.com/pytorch/pytorch/pull/55685))
    * Make `VariableVersion::DISABLED` the default constructor for `VariableVersion`. ([#55572](https://github.com/pytorch/pytorch/pull/55572))
    * Don't set `version_counter` on inference tensor for `unsafe_` ops. ([#55819](https://github.com/pytorch/pytorch/pull/55819))
    * Add & document `borrow_from_optional_tensor` ([#56647](https://github.com/pytorch/pytorch/pull/56647))
    * Migrate hacky wrapper removal to `borrow_from_optional_tensor` ([#56648](https://github.com/pytorch/pytorch/pull/56648))
    * Optimize `at::repeat` ([#56994](https://github.com/pytorch/pytorch/pull/56994))
    * Optimize `intrusive_ptr(TTarget*) ` ctor (`pybind`) ([#57053](https://github.com/pytorch/pytorch/pull/57053))

### torch.fx

* Use precompiled regex in graph name processing ([#52853](https://github.com/pytorch/pytorch/pull/52853)).
* Optimize module path finding in `Tracer` ([#52990](https://github.com/pytorch/pytorch/pull/52990)).
* Speed up `_Namespace.create_name` ([#55580](https://github.com/pytorch/pytorch/pull/55580)).

### Profiler

* Sped up post processing ([#58021](https://github.com/pytorch/pytorch/pull/58021)).

### TorchScript

* Generate arithmetic vs logical right shift as appropriate ([#51749](https://github.com/pytorch/pytorch/pull/51749))
* Introduced likely/unlikely `CompareSelect` hint ([#51751](https://github.com/pytorch/pytorch/pull/51751)).
* Implemented log approximation using the VML approach ([#51752](https://github.com/pytorch/pytorch/pull/51752)).
* Updated `TensorExpr` to use `LLVM` as the default backend ([#52314](https://github.com/pytorch/pytorch/pull/52314)).
* Added support for `aten::hardtanh` (a hot operation in mobilenet v2/v3) ([#52394](https://github.com/pytorch/pytorch/pull/52394))
* Implemented `hardtanh` ([#57750](https://github.com/pytorch/pytorch/pull/57750)).
* Add `aten::batch_norm` into fuser when in inference mode ([#54204](https://github.com/pytorch/pytorch/pull/54204)).
* NNC
    * Added a new API to perform loop fusion ([#54461](https://github.com/pytorch/pytorch/pull/54461)).
    * Implemented depthwise `conv2d` ([#54920](https://github.com/pytorch/pytorch/pull/54920)).
    * Integrated NNC `conv2d` with fuser ([#55213](https://github.com/pytorch/pytorch/pull/55213)).
    * Added logic to use NNC to generate `logit`, `relu` and `tanh` ([#52322](https://github.com/pytorch/pytorch/pull/52322)).
    * Use VML-inspired logarithm with NNC, tweak scheduling ([#52423](https://github.com/pytorch/pytorch/pull/52423)).
    * Generate `sigmoid` with NNC ([#52424](https://github.com/pytorch/pytorch/pull/52424)).
    * Enabled CPU fusion only when `num_threads == 1` ([#56120](https://github.com/pytorch/pytorch/pull/56120)).
    * Use NNC's `call_raw` API to reduce call overheads. ([#57553](https://github.com/pytorch/pytorch/pull/57553)).
    * Started codegen’ing some external calls ([#58118](https://github.com/pytorch/pytorch/pull/58118)).
* Reduce memory use for inference path in `OneDNN MaxPooling` ([#52728](https://github.com/pytorch/pytorch/pull/52728)).
* Removed redundant `gather_ranges` when fusing ([#53323](https://github.com/pytorch/pytorch/pull/53323)).
* Optimized `sigrid_hash` ([#53065](https://github.com/pytorch/pytorch/pull/53065)).
* Updated `create_empty_from` to directly use the native version of `at::empty` ([#53216](https://github.com/pytorch/pytorch/pull/53216)).
* Added a minimum fusion group size ([#50217](https://github.com/pytorch/pytorch/pull/50217)).
* Added CUDNN `Conv-Add-Relu` fusion for Frozen Model Optimization ([#52102](https://github.com/pytorch/pytorch/pull/52102)).
* Avoid dispatch overhead in call to MKLDNN convolution ([#52614](https://github.com/pytorch/pytorch/pull/52614)).
* Added re-inplacing to MKLDNN subgraphs ([#53908](https://github.com/pytorch/pytorch/pull/53908)).
* Set `requires_gradient` to help autodiff prune unneeded gradients ([#54374](https://github.com/pytorch/pytorch/pull/54374)).
* Use type cache in erasing shape information ([#55828](https://github.com/pytorch/pytorch/pull/55828)).
* Added heuristic to avoid perf incompatible MKLDNN formats for binary ops ([#56089](https://github.com/pytorch/pytorch/pull/56089))
* Added `adaptive_avgpool2d` to the set of fusible ops ([#56180](https://github.com/pytorch/pytorch/pull/56180)).
* Lazily initialize `AliasDb` in `remove_mutation` opt ([#55949](https://github.com/pytorch/pytorch/pull/55949))
* Made DataPtr extraction in CUDAFuture faster for Python values ([#56918](https://github.com/pytorch/pytorch/pull/56918)).
* Lazily initialize `AliasDb` in DCE ([#56649](https://github.com/pytorch/pytorch/pull/56649)).
* Add explicit checks for in-place ops in `ReplaceWithCopy` ([#54657](https://github.com/pytorch/pytorch/pull/54657)).
    

### Quantization

* Optimized quantized `torch.cat` ([#54813](https://github.com/pytorch/pytorch/pull/54813)).

### Mobile

* Enabled `QNNPACK` for Apple Silicon builds ([#52308](https://github.com/pytorch/pytorch/pull/52308)).
* Sped up model loading for per-channel quantized models using `QNNPACK` ([#53726](https://github.com/pytorch/pytorch/pull/53726)).
* Added `XNNPACK` implementations for various operationss (`hardswish, global average pool`) ([#56714](https://github.com/pytorch/pytorch/pull/56714), [#56715](https://github.com/pytorch/pytorch/pull/56715), [#55791](https://github.com/pytorch/pytorch/pull/55791)).
* Made various performance improvements for iOS GPU (Metal) ([#57664](https://github.com/pytorch/pytorch/pull/57664), [#57665](https://github.com/pytorch/pytorch/pull/57665), [#57666](https://github.com/pytorch/pytorch/pull/57666), [#57667](https://github.com/pytorch/pytorch/pull/57667), [#57668](https://github.com/pytorch/pytorch/pull/57668)).

### Distributed

`torch.distributed`

* Avoid 2 extra copies when reducing sparse tensors ([#57822](https://github.com/pytorch/pytorch/pull/57822))

### Vulkan

* Switched to a more performant implementation of matrix multiplication ([#49609](https://github.com/pytorch/pytorch/pull/49609)).
* Updated the version of Vulkan Memory Allocator used ([#52938](https://github.com/pytorch/pytorch/pull/52938)).
* Increased the command buffer submission rate ([#57196](https://github.com/pytorch/pytorch/pull/57196)).
* Updated the Vulkan tensors to use 2D textures whenever possible, instead of always using 3D textures ([#57198](https://github.com/pytorch/pytorch/pull/57198)).
* Updated convolution shaders to receive the bias tensor as a texture as opposed to a buffer ([#57201](https://github.com/pytorch/pytorch/pull/57201)).

# Docs

### Python API

* Added `torch.testing` docs ([#57247](https://github.com/pytorch/pytorch/pull/57247)).
* Updated docs to mention CUDA support for Future ([#50048](https://github.com/pytorch/pytorch/pull/50048)).
* Included `memory_format` , an already accepted argument, in `torch.empty` doc ([#54664](https://github.com/pytorch/pytorch/pull/54664)).
* Improved the documentation for torch.matrix_exp() ([#55626](https://github.com/pytorch/pytorch/pull/55626)).
* Updated use_deterministic_algorithms docs ([#55413](https://github.com/pytorch/pytorch/pull/55413)).
* Added the `generator`  argument to `torch.rand` and `torch.randn` docs ([#56242](https://github.com/pytorch/pytorch/pull/56242)).
* Added an example to show how to use learning rate schedulers in Optimizers ([#56705](https://github.com/pytorch/pytorch/pull/56705)).
* Corrected the torch.ceil formula in docs ([#55039](https://github.com/pytorch/pytorch/pull/55039))
* Fixed docs to use autosummary on tensors.rst ([#55042](https://github.com/pytorch/pytorch/pull/55042))
* Improved testing documentation in `CONTRIBUTING.md` ([#54904](https://github.com/pytorch/pytorch/pull/54904))
* Updated `torch.fft` docs to include `out=` argument ([#56732](https://github.com/pytorch/pytorch/pull/56732)).
* Updated rounding_mode documentation to remove `"true"` ([#52202](https://github.com/pytorch/pytorch/pull/52202)).
* Added a note about error handling for non-chained futures ([#53212](https://github.com/pytorch/pytorch/pull/53212)).
* Updated `torch.stft` documentation to clarify output shape ([#54877](https://github.com/pytorch/pytorch/pull/54877)).
* Added an example for `torch.is_tensor` and `torch.is_storage` ([#55052](https://github.com/pytorch/pytorch/pull/55052)).

### Autograd

* Added a note describing gradcheck internals ([#55966](https://github.com/pytorch/pytorch/pull/55966)).
* Split up autograd documentation into separate pages ([#55672](https://github.com/pytorch/pytorch/pull/55672)).
* `torch.utils.checkpoint` : Updated docs to state that `input` flag in `.backward()` is disallowed when checkpointing ([#51746](https://github.com/pytorch/pytorch/pull/51746)).
* Added section in autograd mechanics note describing how to use inference/no_grad ([#58513](https://github.com/pytorch/pytorch/pull/58513)).
* Added doc string for `torch.is_inference_mode_enabled` and `torch.is_grad_enabled` ([#59047](https://github.com/pytorch/pytorch/pull/59047)).
* Added no-grad inference mode note ([#58513](https://github.com/pytorch/pytorch/pull/58513)).
* Add docstring for is_inference_mode_enabled ([#59047](https://github.com/pytorch/pytorch/pull/59047)).

### torch.nn

* `nn.TripletMarginLoss` / `torch.reciprocal`: Fix formatting in docs ([#51650](https://github.com/pytorch/pytorch/pull/51650))
* `nn.FractionalMaxPool3d`: Add to pooling layer docs ([#52556](https://github.com/pytorch/pytorch/pull/52556))
* `F.fractional_max_pool`: Add to `nn.functional` docs ([#52557](https://github.com/pytorch/pytorch/pull/52557))
* `Module.share_memory`: Add link to `Tensor.share_memory_` in docs ([#52561](https://github.com/pytorch/pytorch/pull/52561))
* `nn.SiLU`: Mention alternative name of Swish within docs ([#53239](https://github.com/pytorch/pytorch/pull/53239))
* Remove redundant hardsigmoid() in docstring to show up `inplace` parameter ([#52559](https://github.com/pytorch/pytorch/pull/52559))
* Clarify docs for lazy modules ([#53495](https://github.com/pytorch/pytorch/pull/53495))
* `torch.nn`: Grammatically update docs ([#54370](https://github.com/pytorch/pytorch/pull/54370))
* `nn.Sequential`: Expand docs, including comparison with `nn.ModuleList` ([#53380](https://github.com/pytorch/pytorch/pull/53380))
* `F.embedding_bag`: Fix formatting in docs ([#54666](https://github.com/pytorch/pytorch/pull/54666))
* `F.group_norm`: Add to docs ([#54673](https://github.com/pytorch/pytorch/pull/54673))
* Add separate autosummary for flatten layer docs ([#54663](https://github.com/pytorch/pytorch/pull/54663))
* `LazyModuleMixin`: Add missing attr in docs to improve formatting ([#53363](https://github.com/pytorch/pytorch/pull/53363))
* `conv1d`: Fix example error in docs ([#57356](https://github.com/pytorch/pytorch/pull/57356))
* `nn.functional`: Split docs into a table-of-contents page and a sub-page per function ([#55038](https://github.com/pytorch/pytorch/pull/55038))
* `nn.LSTM` / `nn.RNN` / `nn.GRU`: Clarify `batch_first` behavior ([#58809](https://github.com/pytorch/pytorch/pull/58809))
* `nn.CosineEmbeddingLoss`: Add shape info to docs ([#58403](https://github.com/pytorch/pytorch/pull/58403))
* Add doc warnings for default SELU gain ([#54057](https://github.com/pytorch/pytorch/pull/54057)).
* Clarify batch_first behavior for `nn.LSTM, nn.RNN, and nn.GRU` ([#58809](https://github.com/pytorch/pytorch/pull/58809)).
* Add UninitializedBuffer to nn docs ( [#59021](https://github.com/pytorch/pytorch/pull/59021)).
* Document factory_kwargs in nn.Quantize + remove Attributes section ([#59025](https://github.com/pytorch/pytorch/pull/59025)).

### Dataloader

* Added DataPipes Typing Doc ([#54773](https://github.com/pytorch/pytorch/pull/54773)).
* Added docs to document the default NumPy seed for DataLoader workers ([#56528](https://github.com/pytorch/pytorch/pull/56528)).

### AMD

* Added HIP semantics doc ([#57871](https://github.com/pytorch/pytorch/pull/57871)).

### CUDA

* Added `scatter_add` to amp docs ([#54908](https://github.com/pytorch/pytorch/pull/54908)) 
* Added `reset_peak_memory_stats` in cuda.rst ([#54668](https://github.com/pytorch/pytorch/pull/54668)).

### torch.fx

* Make some modifications to limitation section ([#51928](https://github.com/pytorch/pytorch/pull/51928))
* Added docstring for concrete_args on `Tracer.trace` ([#53151](https://github.com/pytorch/pytorch/pull/53151)).
* Change Dynamic Control Flow example to a *more* dynamic version ([#53250](https://github.com/pytorch/pytorch/pull/53250)).
* Render inherited methods in fx.Tracer API reference ([#53630](https://github.com/pytorch/pytorch/pull/53630)).
* Add docs for `ShapeProp` ([#54554](https://github.com/pytorch/pytorch/pull/54554)).
* Hide module paths leaking in the documentation. ([#54585](https://github.com/pytorch/pytorch/pull/54585)).

### Profiler

* Updated profiler recipe doc (https://github.com/pytorch/tutorials/pull/1528).

### TorchScript

* Added NNC IR specification ([#52912](https://github.com/pytorch/pytorch/pull/52912)).
* Added starter content for new TorchScript language reference ([#53837](https://github.com/pytorch/pytorch/pull/53837)).
* Added documentation for `torch.jit.Attribute` and `torch.jit.annotate` ([#54485](https://github.com/pytorch/pytorch/pull/54485)).
* Updated TorchScript language reference section for types ([#53673](https://github.com/pytorch/pytorch/pull/53673)).
* Documented the TorchScript type system ([#53244](https://github.com/pytorch/pytorch/pull/53244)).
* Added language reference for Python builtin functions, statements,  and values in TorchScript ([#52847](https://github.com/pytorch/pytorch/pull/52847), [#52830](https://github.com/pytorch/pytorch/pull/52830)).
* Added `torch.*` API section for TorchScript language reference ([#53236](https://github.com/pytorch/pytorch/pull/53236)).
* Added “Conditionals in TE” doc ([#56949](https://github.com/pytorch/pytorch/pull/56949)).
    

### torch.package

* Added API reference ([#55812](https://github.com/pytorch/pytorch/pull/55812), [#56547](https://github.com/pytorch/pytorch/pull/56547)).
* Add explanation, tutorial, and preamble sections for `torch.package` ([#59833](https://github.com/pytorch/pytorch/pull/59833), [#59503](https://github.com/pytorch/pytorch/pull/59503), [#59499](https://github.com/pytorch/pytorch/pull/59499), [#59491](https://github.com/pytorch/pytorch/pull/59491), [#59842](https://github.com/pytorch/pytorch/pull/59842), [#59843](https://github.com/pytorch/pytorch/pull/59843), [#59602](https://github.com/pytorch/pytorch/pull/59602)).
* Add pickle security warning to package docs ([#59959](https://github.com/pytorch/pytorch/pull/59959)).

### Quantization

* Added docs for storage and tensors for quantized Tensor ([#51817](https://github.com/pytorch/pytorch/pull/51817)).
* Fixed FX Graph Mode Quantization tutorial link ([#54715](https://github.com/pytorch/pytorch/pull/54715)).
* Added fx graph mode quant api doc ([#55306](https://github.com/pytorch/pytorch/pull/55306)).
* FX Graph Mode Quantization - fixed preamble ([#52192](https://github.com/pytorch/pytorch/pull/52192)).
* Fixed broken link to fx graph quant guide in quantization.rst ([#56776](https://github.com/pytorch/pytorch/pull/56776)).

### Mobile

* Added doc string for lite interpreter related API in Android ([#53136](https://github.com/pytorch/pytorch/pull/53136)).
* Improved `export_opnames` Documentation ([#52333](https://github.com/pytorch/pytorch/pull/52333)).

### Distributed

`torch.distributed.Store`

* Documentation for TCPStore’s `compare_set` API ([#57203](https://github.com/pytorch/pytorch/pull/57203))

`torch.distributed.optim`

* Update distributed optimizer documentation ([#58084](https://github.com/pytorch/pytorch/pull/58084))
* Update and expose ZeroRedundancyOptimizer docs ([#53112](https://github.com/pytorch/pytorch/pull/53112), [#53113](https://github.com/pytorch/pytorch/pull/53113))


`torch.distributed.elastic`

* Upstream `torchelastic` documentation to PyTorch. ([#56811](https://github.com/pytorch/pytorch/pull/56811))
* Revise the note section of RendezvousHandler doc ([#57723](https://github.com/pytorch/pytorch/pull/57723))
* Update the rendezvous documentation ([#57973](https://github.com/pytorch/pytorch/pull/57973))


`DistributedDataParallel`

* Add register_comm_hook API to DDP communication hooks documentation page ([#51846](https://github.com/pytorch/pytorch/pull/51846),[](https://github.com/pytorch/pytorch/pull/51986)[#51986](https://github.com/pytorch/pytorch/pull/51986))
* Enhance documentation around `DistributedDataParallel` uneven input support ([#57448](https://github.com/pytorch/pytorch/pull/57448))
* Enhance communication hook documentation ([#58170](https://github.com/pytorch/pytorch/pull/58170), [#58168](https://github.com/pytorch/pytorch/pull/58168), [#53253](https://github.com/pytorch/pytorch/pull/53253), [#53855](https://github.com/pytorch/pytorch/pull/53855), [#53596,](https://github.com/pytorch/pytorch/pull/53596)[#53955](https://github.com/pytorch/pytorch/pull/53955), [#54052](https://github.com/pytorch/pytorch/pull/54052). [#55031](https://github.com/pytorch/pytorch/pull/55031))


`torch.distributed.rpc`

* Add a disclaimer about limited CUDA support in RPC ([#58023](https://github.com/pytorch/pytorch/pull/58023)) 
* `torch.distributed.rpc`:  Add a link to the tutorial in RemoteModule docstring ([#57875](https://github.com/pytorch/pytorch/pull/57875))
* `torch.distributed.rpc`:  Mentioned `RemoteModule` in RPC documentation ([#57876](https://github.com/pytorch/pytorch/pull/57876))


`torch.distributed.nn.RemoteModule`

* Add RemoteModule to master RPC docs. ([#53084](https://github.com/pytorch/pytorch/pull/53084))
* Add `remote_parameters` and `get_module_rref` to RemoteModule docs. ([#54645](https://github.com/pytorch/pytorch/pull/54645))

`torch.distributed.pipeline`

* Enhance Pipe docs to explicitly mention RPC initialization. ([#55187](https://github.com/pytorch/pytorch/pull/55187))
* Add tutorials to pipeline docs. ([#55209](https://github.com/pytorch/pytorch/pull/55209))

`torch.distributed`

* Update documentation for `get_future` support ([#58107](https://github.com/pytorch/pytorch/pull/58107))
* Mention distributed profiling in documentation ([#58286](https://github.com/pytorch/pytorch/pull/58286))
* Update distributed doc table for `alltoall`  ([#54277](https://github.com/pytorch/pytorch/pull/54277))
*  fix docstring signature in `all_reduce_multigpu` ([#54665](https://github.com/pytorch/pytorch/pull/54665))
* `torch.distributed`: Improve dist.new_group doc ([#55660](https://github.com/pytorch/pytorch/pull/55660))

### ONNX

* Updated ONNX documentation ([#51362](https://github.com/pytorch/pytorch/pull/51362)) ([#53313](https://github.com/pytorch/pytorch/pull/53313)).
* Updated scripting docs ([#54634](https://github.com/pytorch/pytorch/pull/54634)) ([#54868](https://github.com/pytorch/pytorch/pull/54868)).
* Fixed docstring signature of torch.{onnx,utils} ([#54662](https://github.com/pytorch/pytorch/pull/54662)).
* onnx.symbolic_helper.parse_args: document and clean up ([#56956](https://github.com/pytorch/pytorch/pull/56956)) ([#57598](https://github.com/pytorch/pytorch/pull/57598)).


# ===== RELEASE pytorch/pytorch v1.10.0 =====

# 1.10.0 Release Notes

* Highlights
* Backwards Incompatible Change
* New Features
* Improvements
* Performance
* Documentation

# Highlights

We are excited to announce the release of PyTorch 1.10. This release is composed of over 3,400 commits since 1.9, made by 426 contributors. We want to sincerely thank our community for continuously improving PyTorch. 

PyTorch 1.10 updates are focused on improving training and performance of PyTorch, and developer usability. Highlights include:
* CUDA Graphs APIs are integrated to reduce CPU overheads for CUDA workloads.
* Several frontend APIs such as FX, `torch.special`, and `nn.Module` Parametrization, have moved from beta to stable.  
* Support for automatic fusion in JIT Compiler expands to CPUs in addition to GPUs.
* Android NNAPI support is now available in beta.

You can check the blogpost that shows the new features [here](https://pytorch.org/blog/pytorch-1.10-released/).

# Backwards Incompatible changes

## Python API

### `torch.any`/`torch.all` behavior changed slightly to be more consistent for zero-dimension, `uint8` tensors. ([#64642](https://github.com/pytorch/pytorch/pull/64642))

These two functions match the behavior of NumPy, returning an output dtype of bool for all support dtypes, except for `uint8` (in which case they return a 1 or a 0, but with `uint8` dtype). In some cases with 0-dim tensor inputs, the returned `uint8` value could mistakenly take on a value > 1. This has now been fixed.

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> torch.all(torch.tensor(42, dtype=torch.uint8))
tensor(1, dtype=torch.uint8)
>>> torch.all(torch.tensor(42, dtype=torch.uint8), dim=0)
tensor(42, dtype=torch.uint8) # wrong, old behavior
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> torch.all(torch.tensor(42, dtype=torch.uint8))
tensor(1, dtype=torch.uint8)
>>> torch.all(torch.tensor(42, dtype=torch.uint8), dim=0)
tensor(1, dtype=torch.uint8) # new, corrected and consistent behavior
      </pre></sub></td>
    </tr>
  </table>
</p>

### Remove deprecated `torch.{is,set}_deterministic` ([#62158](https://github.com/pytorch/pytorch/pull/62158))

This is the end of the deprecation cycle for both of these functions. You should be using `torch.use_deterministic_algorithms` and`torch.are_deterministic_algorithms_enabled` instead.

## Complex Numbers

### **Conjugate View: [`tensor.conj()`](https://pytorch.org/docs/1.10./generated/torch.conj.html) now returns a view tensor that aliases the same memory and has conjugate bit set ([#54987](https://github.com/pytorch/pytorch/pull/54987), [#60522](https://github.com/pytorch/pytorch/pull/60522), [#66082](https://github.com/pytorch/pytorch/pull/66082), [#63602](https://github.com/pytorch/pytorch/pull/63602)).** 

This means that `.conj()` is now an O(1) operation and returns a tensor that views the same memory as `tensor` and has conjugate bit set. This notion of conjugate bit enables fusion of operations with conjugation which gives a lot of performance benefit for operations like matrix multiplication. All out-of-place operations will have the same behavior as before, but an in-place operation on a conjugated tensor will additionally modify the input tensor. 

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> import torch
>>> x = torch.tensor([1+2j])
>>> y = x.conj()
>>> y.add_(2)
>>> print(x)
tensor([1.+2.j])
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> import torch
>>> x = torch.tensor([1+2j])
>>> y = x.conj()
>>> y.add_(2)
>>> print(x)
tensor([3.+2.j])
      </pre></sub></td>
    </tr>
  </table>
</p>

Note: You can verify if the conj bit is set by calling `tensor.is_conj()`. The conjugation can be resolved, i.e., you can obtain a new tensor that doesn’t share storage with the input tensor at any time by calling `conjugated_tensor.clone()` or `conjugated_tensor.resolve_conj()` .

Note that these conjugated tensors behave differently from the corresponding numpy arrays obtained from `np.conj()` when an in-place operation is performed on them (similar to the example shown above).


### **Negative View: `tensor.conj().neg()` returns a view tensor that aliases the same memory as both tensor and `tensor.conj()` and has a negative bit set ([#56058](https://github.com/pytorch/pytorch/pull/56058)).**

`conjugated_tensor.neg()` continues to be an O(1) operation, but the returned tensor shares memory with both `tensor` and `conjugated_tensor`.

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> x = torch.tensor([1+2j])
>>> y = x.conj()
>>> z = y.imag
>>> z.add_(2)
>>> print(x)
tensor([1.+2.j])
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> x = torch.tensor([1+2j])
>>> y = x.conj()
>>> z = y.imag
>>> print(z.is_neg())
True
>>> z.add_(2)
>>> print(x)
tensor([1.-0.j])
      </pre></sub></td>
    </tr>
  </table>
</p>


### `tensor.numpy()` now throws `RuntimeError` when called on a tensor with conjugate or negative bit set ([#61925](https://github.com/pytorch/pytorch/pull/61925)).

Because the notion of conjugate bit and negative bit doesn’t exist outside of PyTorch, calling operations that return a Python object viewing the same memory as input like `.numpy()` would no longer work for tensors with conjugate or negative bit set.

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
>>> x = torch.tensor([1+2j])
>>> y = x.conj().imag
>>> print(y.numpy())
[2.]
      </pre></sub></td>
      <td><sub><pre lang="python">
>>> x = torch.tensor([1+2j])
>>> y = x.conj().imag
>>> print(y.numpy())
RuntimeError: Can't call numpy() on Tensor that has negative
bit set. Use tensor.resolve_neg().numpy() instead.
      </pre></sub></td>
    </tr>
  </table>
</p>

## Autograd

### Raise `TypeError` instead of `RuntimeError` when assigning to a Tensor’s grad field with wrong type ([#64876](https://github.com/pytorch/pytorch/pull/64876))

Setting the `.grad` field with a non-None and non-Tensor object used to return a `RuntimeError` but it now properly returns a `TypeError`. If your code was catching this error, you should simply update it to catch a `TypeError` instead of a `RuntimeError`.

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
try:
    # Assigning an int to a Tensor's grad field
    a.grad = 0
except RuntimeError as e:
    pass
      </pre></sub></td>
      <td><sub><pre lang="python">
try:
   a.grad = 0
except TypeError as e:
    pass
      </pre></sub></td>
    </tr>
  </table>
</p>

### Raise error when inputs to `autograd.grad` are empty ([#52016](https://github.com/pytorch/pytorch/pull/52016))

Calling `autograd.grad` with an empty list of inputs used to do the same as backward. To reduce confusion, it now raises the expected error. If you were relying on this, you can simply update your code as follows:

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
grad = autograd.grad(out, tuple())
assert grad == tuple()
      </pre></sub></td>
      <td><sub><pre lang="python">
out.backward()
      </pre></sub></td>
    </tr>
  </table>
</p>


### Optional arguments to `autograd.gradcheck` and `autograd.gradgradcheck` are now kwarg-only ([#65290](https://github.com/pytorch/pytorch/pull/65290))

These two functions now have a significant number of optional arguments controlling what they do (i.e., `eps`, `atol`, `rtol`, `raise_exception`, etc.). To improve readability, we made these arguments kwarg-only. If you are passing these arguments to `autograd.gradcheck` or `autograd.gradgradcheck` as positional arguments, you can update your code as follows:

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
torch.autograd.gradcheck(fn, x, 1e-6)
      </pre></sub></td>
      <td><sub><pre lang="python">
torch.autograd.gradcheck(fn, x, eps=1e-6)
      </pre></sub></td>
    </tr>
  </table>
</p>


### In-place detach (`detach_`) now errors for views that return multiple outputs ([#58285](https://github.com/pytorch/pytorch/pull/58285))

This change is finishing the deprecation cycle for the inplace-over-view logic. In particular, a few things that were warning are updated:

    * `detach_` will now raise an error when invoked on any view created by `split`, `split_with_sizes`, or `chunk`. You should use the non-inplace `detach` instead.
    * The error message for when an in-place operation (that is not detach) is performed on a view created by `split`, `split_with_size`, and `chunk` has been changed from "This view is an output of a function..." to "This view is the output of a function...".

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
b = a.split(1)[0]
b.detach_()
      </pre></sub></td>
      <td><sub><pre lang="python">
b = a.split(1)[0]
c = b.detach()
      </pre></sub></td>
    </tr>
  </table>
</p>

### Fix saved variable unpacking version counter ([#60195](https://github.com/pytorch/pytorch/pull/60195))

In-place on the unpacked SavedVariables used to be ignored. They are now properly detected which can lead to errors saying that a variable needed for backward was modified in-place.
This is a valid error and the user should fix this by cloning the unpacked saved variable before using it.

No internal formula will trigger this, but it might be triggered by user custom `autograd.Function` if the backward modifies a saved Tensor inplace and you do multiple backwards. This used to silently return the wrong result and will now raise the expected error.

## torch.nn

### Added optional tensor arguments to `__torch_function__` handling checks ([#63967](https://github.com/pytorch/pytorch/pull/63967))

This fixes the `has_torch_function*()` checks throughout `torch.nn.functional` to correctly pass in optional tensor arguments; prior to this fix, `handle_torch_function()` was not called for these optional tensor arguments. Previously, passing a tensor-like object into a function that accepts an optional tensor might not trigger that object's `__torch_function__`. Now, the object's `__torch_function__` will be triggered as expected.

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
import torch
import torch.nn.functional as F
class TestTensor(object):
    def __init__(self, weight):
        self.weight = weight
    def __torch_function__(self, func, _, args=(), kwargs=None):
        print(func)
        print(func == F.group_norm)
# Call F.group_norm with a custom Tensor as the non-optional arg 'features'
features = TestTensor(torch.randn(3,3))
F.group_norm(features, 3)
# ...prints "group_norm" and True
# Call F.group_norm with a custom Tensor as the optional arg 'weight'
features = torch.randn(3,3)
weight = TestTensor(torch.randn(3))
F.group_norm(features, 3, weight=weight)
# ...prints "group_norm" and False because weight's __torch_function__ is
# called with func as torch.group_norm instead of F.group_norm
      </pre></sub></td>
      <td><sub><pre lang="python">
import torch
import torch.nn.functional as F
class TestTensor(object):
    def __init__(self, weight):
        self.weight = weight
    def __torch_function__(self, func, _, args=(), kwargs=None):
        print(func)
        print(func == F.group_norm)
# Call F.group_norm with a custom Tensor as the non-optional arg 'features'
features = TestTensor(torch.randn(3,3))
F.group_norm(features, 3)
# ...prints "group_norm" and True
# Call F.group_norm with a custom Tensor as the optional arg 'weight'
features = torch.randn(3,3)
weight = TestTensor(torch.randn(3))
F.group_norm(features, 3, weight=weight)
# ...prints "group_norm" and True
      </pre></sub></td>
    </tr>
  </table>
</p>

## CUDA

### Removed post-backward syncs on default stream ([#60421](https://github.com/pytorch/pytorch/pull/60421))

Calls to backward() or grad() synced only the calling thread's default stream with autograd leaf streams at the end of backward. This made the following weird pattern safe:

```python
with torch.cuda.stream(s):
    # imagine forward used many streams, so backward leaf nodes may run on many streams
    loss.backward()# no sync
use grads
```

but a more benign-looking pattern was unsafe:

```python
with torch.cuda.stream(s):
    # imagine forward used a lot of streams, so backward leaf nodes may run on many streams
    loss.backward()
    # backward() syncs the default stream with all the leaf streams, but does not sync s with anything,
    # so counterintuitively (even though we're in the same stream context as backward()!)
    # it is NOT SAFE to use grads here, and there's no easy way to make it safe,
    # unless you manually sync on all the streams you used in forward,
    # or move "use grads" back to default stream outside the context.
    use grads
```

Note: this change makes it so that backward() has [same user-facing stream semantics as any cuda op](https://pytorch.org/docs/master/notes/cuda.html#stream-semantics-of-backward-passes).** In other words, the weird pattern is unsafe, and the benign-looking pattern is safe. Implementation-wise, this meant backward() should sync its calling thread's current stream, not default stream, with the leaf streams. This PR  deletes syncs on the default stream. 

## torch.package

* Removed verbose mode from PackageExporter ([#61145](https://github.com/pytorch/pytorch/pull/61145))
    * PackageExporter is losing “verbose” mode argument as we have found it is not useful and sometimes confusing. See following examples on how to modify your code to accommodate this change.

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
with PackageExporter(buffer, verbose=False) as e:
    e.intern("**")
    e.save_pickle("res", "mod1.pkl", mod1)
    e.save_pickle("res", "mod2.pkl", mod2)
      </pre></sub></td>
      <td><sub><pre lang="python">
with PackageExporter(buffer) as e:
    e.intern("**")
    e.save_pickle("res", "mod1.pkl", mod1)
    e.save_pickle("res", "mod2.pkl", mod2)
      </pre></sub></td>
    </tr>
  </table>
</p>


## Quantization

### Added extra observer/fake_quant (the same observer/fake_quant instance as the input) for some operators in prepare_fx, e.g. maxpool, add_scalar and mul_scalar ([#61687](https://github.com/pytorch/pytorch/pull/61687), [#61859](https://github.com/pytorch/pytorch/pull/61859))

Previously the way we insert observers/fake_quants are specific to fbgemm/qnnpack backend, as we work on making FX Graph Mode Quantization extensible to custom backends, we are changing some behaviors for the fbgemm/qnnpack path as well. The above changes are adding extra observer/fake_quant to the output of some operators to make sure we model the quantized operator more accurately in quantization aware training, the comprehensive list of operators where the behavior changes are the following:

* modules: torch.nn.MaxPool1d, torch.nn.MaxPool2d, torch.nn.MaxPool3d, torch.nn.Identity
* torch functions: torch.nn.functional.max_pool1d, torch.nn.functional.max_pool2d, torch.nn.functional.max_pool3d, torch.chunk, torch.flatten, torch.transpose, torch.repeat_interleave, torch.sort, torch.squeeze, torch.stack, torch.unsqueeze, operator.getitem, 
* Tensor methods: chunk, contiguous, detach, detach_, numel, permute, repeat, repeat_interleave, reshape, resize_, shape, size, squeeze, squeeze_, transpose, unsqueeze, unsqueeze_, view
* Tensor operations: add scalar and mul scalar (add/mul with a Tensor and a Scalar input)


We will show an example with torch.nn.MaxPool2d:

```python
class M(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.maxpool2d = torch.nn.MaxPool2d(kernel_size=3)

    def forward(self, x):
        x = self.maxpool2d(x)
        return x
m = M().eval()        
m = prepare_fx(m, {"": torch.quantization.default_qconfig})
print(m.code)
```

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
def forward(self, x):
    x_activation_post_process_0 = self.x_activation_post_process_0(x); x = None
    maxpool2d = self.maxpool2d(x_activation_post_process_0); x_activation_post_process_0 = None
    return maxpool2d
      </pre></sub></td>
      <td><sub><pre lang="python">
def forward(self, x):
    x_activation_post_process_0 = self.x_activation_post_process_0(x); x = None
    maxpool2d = self.maxpool2d(x_activation_post_process_0); x_activation_post_process_0 = None
    maxpool2d_activation_post_process_0 = self.maxpool2d_activation_post_process_0(maxpool2d); maxpool2d = None
    return maxpool2d_activation_post_process_0
      </pre></sub></td>
    </tr>
  </table>
</p>

Note that `self.maxpool2d_activation_post_process_0` and `self.x_activation_post_process_0` will refer to the same observer/fake_quant instance, this is to simulate the numerics for the quantized maxpool implementation, where the output would reuse the quantization parameter of the input. Simple illustration with graph:

Before:

```
observer_0 - maxpool - ...
```

After:

```
observer_0 - maxpool - observer_0 (same observer instance as input observer) - ...
```

## ONNX

### Removed `aten` arg from `torch.onnx.export()`. ([#62759](https://github.com/pytorch/pytorch/pull/62759))

The new `OperatorExportTypes.ONNX` removes the need for an explicit `aten` argument. If Pytorch was built with `-DPYTORCH_ONNX_CAFFE2_BUNDLE` the a `None` value means `OperatorExportTypes.ONNX_ATEN_FALLBACK`

<p align="center">
  <table align="center">
    <tr><th>1.9.1</th><th>1.10.0</th></tr>
    <tr valign="top">
      <td><sub><pre lang="python">
torch.onnx.export(..., aten=True)
      </pre></sub></td>
      <td><sub><pre lang="python">
torch.onnx.export(..., operator_export_type=torch.onnx.OperatorExportTypes.ONNX_ATEN)
      </pre></sub></td>
    </tr>
  </table>
</p>

# Deprecations

## Python API

### Deprecate **`__torch_function__`** as a plain methods ([#64843](https://github.com/pytorch/pytorch/pull/64843))

The `__torch_function__` function used to create Tensor like objects did not have any constraint whether it should be a method, class method or static method.

To make it compatible with newer features on Tensor-like objects, we are deprecating setting it as a plain method. You can define it as a class method to get the current class and scan the argument list if you need an object that is an instance of this class.

## Mobile

### Removed API torch.utils.bundled_inputs.run_on_bundled_input ([#58344](https://github.com/pytorch/pytorch/pull/58344))

This API caused many issues and is not really necessary. The functionality (run model with bundled input) can be achieved by using `get_all_bundled_inputs`. For example:

1.9.1:

```python
model.run_on_bundled_input(0)
```

1.10.0:

```python
model(*model.get_all_bundled_inputs()[0])
```

## Distributed

### `torch.distributed.rpc`: Removed ProcessGroup RPC backend ([#62411](https://github.com/pytorch/pytorch/pull/62411) , [#62985](https://github.com/pytorch/pytorch/pull/62985))

ProcessGroup RPC backend has been deprecated and 1.9 was the last release which carried it. The default RPC backend is TensorPipe which is the recommended backend for RPC. Users who use `torch.distributed.rpc.BackendType.PROCESS_GROUP` will be given an error message to switch to `torch.distributed.rpc.BackendType.TENSORPIPE`.

## ONNX

### Removed following arguments in torch.onnx.export(): enable_onnx_checker, strip_doc_string, _retain_param_name  ([#64369](https://github.com/pytorch/pytorch/pull/64369), [#64371](https://github.com/pytorch/pytorch/pull/64371), [#64370](https://github.com/pytorch/pytorch/pull/64370))

`enable_onnx_checker` argument is removed. ONNX checker will now always run by default. Users can catch exceptions to ignore raised failures. `strip_doc_string` has been rolled into the `verbose` arg in `torch.onnx.export()`. `_retain_param_name` argument has been removed in  `torch.onnx.export()` will default to `True` . There is no way to get the old behavior of `_retain_param_name=False`. Users should stop setting this arg.

1.9.1:

```
torch.onnx.export(..., enable_onnx_checker=False, strip_doc_string=False)
```

1.10.0:

```
try:
    torch.onnx.export(verbose=True)
except torch.onnx.utils.ONNXCheckerError:
   pass
```

## Infra (Releng)

### Disable ParallelTBB ([#65092](https://github.com/pytorch/pytorch/pull/65092))

`ParallelTBB` config/codepath is no longer actively tested by PyTorch CI and as result is subject to code/functionality degradation


# New features

## Python API

* Added new functions:
    *  `torch.isin()` ([#53125](https://github.com/pytorch/pytorch/pull/53125)), `torch.bitwise_{left/right}_shift`, `__rlshift__`, `__rrshift__` ([#59544](https://github.com/pytorch/pytorch/pull/59544)), `torch.Tensor.{__rand__, __ror__,__rxor__}` ([#59240](https://github.com/pytorch/pytorch/pull/59240)),  `torch.aminmax` ([#62401](https://github.com/pytorch/pytorch/pull/62401)),  `torch.new_ones` ([#58405](https://github.com/pytorch/pytorch/pull/58405))
    * For numpy compatibility `torch.cov` ([#58311](https://github.com/pytorch/pytorch/pull/58311)), `torch.frombuffer` ([#59077](https://github.com/pytorch/pytorch/pull/59077)), `torch.corrcoef` ([#60420](https://github.com/pytorch/pytorch/pull/60420)), `torch.nanmean` ([#62671](https://github.com/pytorch/pytorch/pull/62671)), `torch.cumulative_trapezoid` ([#61615](https://github.com/pytorch/pytorch/pull/61615))
* The [torch.special module](https://pytorch.org/docs/1.10.0/special.html?highlight=special) is now stable! This module, consistent with SciPy’s special module, has 30 operations including the Hurwitz zeta function and various gamma functions.  ([#59623](https://github.com/pytorch/pytorch/pull/59623), [#56352](https://github.com/pytorch/pytorch/pull/56352), [#58126](https://github.com/pytorch/pytorch/pull/58126), [#59141](https://github.com/pytorch/pytorch/pull/59141), [#59143](https://github.com/pytorch/pytorch/pull/59143), [#58650](https://github.com/pytorch/pytorch/pull/58650), [#55878](https://github.com/pytorch/pytorch/pull/55878), [#58838](https://github.com/pytorch/pytorch/pull/58838), [#60512](https://github.com/pytorch/pytorch/pull/60512), [#60641](https://github.com/pytorch/pytorch/pull/60641), [#61633](https://github.com/pytorch/pytorch/pull/61633), [#60519](https://github.com/pytorch/pytorch/pull/60519), [#59691](https://github.com/pytorch/pytorch/pull/59691), [#58194](https://github.com/pytorch/pytorch/pull/58194))
* Added support for slots and subclass magic getstate/setstate method for Tensor serialization ([#62745](https://github.com/pytorch/pytorch/pull/62745))
* `torch.optim`:
    * Added Nesterov Adam as `NAdam` ([#59009](https://github.com/pytorch/pytorch/pull/59009))
    * Added `lr_scheduler.ChainedScheduler` ([#63491](https://github.com/pytorch/pytorch/pull/63491), [#63457](https://github.com/pytorch/pytorch/pull/63457), [#65034](https://github.com/pytorch/pytorch/pull/65034)))
    * Added `lr_scheduler.SequentialLR` ([#64037](https://github.com/pytorch/pytorch/pull/64037), [#65035](https://github.com/pytorch/pytorch/pull/65035))
    * Added `lr_scheduler.{ConstantLR,LinearLR}` ([#64395](https://github.com/pytorch/pytorch/pull/64395))
* `torch.cpu.amp.autocast`: enable new API for CPU autocast ([#57386](https://github.com/pytorch/pytorch/pull/57386), [#63534](https://github.com/pytorch/pytorch/pull/63534))
* Added `BFloat16` support for `torch.{cross, tril, triu, tril_indices, triu_indices, cumsum, cummax, cummin, median, kthvalue, nansum, nextafter, range, sinh, cosh, frexp, nan_to_num, sigmoid, sigmoid_backward, tanh_backward, addcmul, addcdiv, bucketize, bernoulli, dropout, fold, unfold, MaxPool2D, AdaptiveAvgPool2D, topk}` on CPU ([#62454](https://github.com/pytorch/pytorch/pull/62454), [#63307](https://github.com/pytorch/pytorch/pull/63307), [#55210](https://github.com/pytorch/pytorch/pull/55210), [#60074](https://github.com/pytorch/pytorch/pull/60074), [#61083](https://github.com/pytorch/pytorch/pull/61083), [#61829](https://github.com/pytorch/pytorch/pull/61829), [#55221](https://github.com/pytorch/pytorch/pull/55221),  [#61826](https://github.com/pytorch/pytorch/pull/61826), [#55588](https://github.com/pytorch/pytorch/pull/55588), [#56372](https://github.com/pytorch/pytorch/pull/56372), [#62880](https://github.com/pytorch/pytorch/pull/62880), [#55202](https://github.com/pytorch/pytorch/pull/55202), [#59547](https://github.com/pytorch/pytorch/pull/59547))
* Added `BFloat16` support for  `torch.{ceil, floor, frac, round, trunc, sort, topk, aminmax, cumsum, logcumsumexp, cumprod, cummin, cummax}` on CUDA ([#57910](https://github.com/pytorch/pytorch/pull/57910), [#58196](https://github.com/pytorch/pytorch/pull/58196), [#59977](https://github.com/pytorch/pytorch/pull/59977), [#62767](https://github.com/pytorch/pytorch/pull/62767), [#57904](https://github.com/pytorch/pytorch/pull/57904)).
* Added  `torch.cuda.is_bf16_supported` ([#63798](https://github.com/pytorch/pytorch/pull/63798))
* Added zero rate to Poisson distribution ([#61511](https://github.com/pytorch/pytorch/pull/61511))
* Added `torch.segment_reduce` ([#59951](https://github.com/pytorch/pytorch/pull/59951), [#60018](https://github.com/pytorch/pytorch/pull/60018), [#61141](https://github.com/pytorch/pytorch/pull/61141), [#61266](https://github.com/pytorch/pytorch/pull/61266), [#59521](https://github.com/pytorch/pytorch/pull/59521), [#60379](https://github.com/pytorch/pytorch/pull/60379), [#60379](https://github.com/pytorch/pytorch/pull/60379))
* Added boolean support to `torch.isclose` ([#61271](https://github.com/pytorch/pytorch/pull/61271))
* Added `torch.trapezoid` ([#61475](https://github.com/pytorch/pytorch/pull/61475)).
* Added `torch.gradient` support for second order central differences (edge_order=2) ([#58165](https://github.com/pytorch/pytorch/pull/58165))
* `torch.sigmoid`: CUDA support and complex autograd support ([#48647](https://github.com/pytorch/pytorch/pull/48647))
* Added channels-last support for `torch.bilinear` and `torch.nn,MaxUnpool2d` ([#56322](https://github.com/pytorch/pytorch/pull/56322), [#49984](https://github.com/pytorch/pytorch/pull/49984))

## Autograd

* [Experimental] Forward mode AD:
    * *NOTE: In addition to operators listed below, many simple ops are already supported. If you encounter an operator that does not have a forward-mode AD formula implemented, please file an issue. As a workaround, you can use custom `autograd.Function` to implement your own forward-mode-AD-supported operator.*
    * Added forward-mode AD support for custom `autograd.Function` ([#64061](https://github.com/pytorch/pytorch/pull/64061), [#63434](https://github.com/pytorch/pytorch/pull/63434))
    * Added forward-mode AD support for `torch.{acos, add, addbmm, addcdiv, addcmul, addmm, addmv, addr, angle, acosh, asinh, atanh, asin, atan, conj, baddbmm, bmm, cat, ceil, clamp, clamp_min, clamp_max, complex, copy_sign, cos, cosh, cross, cumprod, cumsum, cummax, cummin, deg2rad, div, dot, vdot, exp, exp2, expm1, expand, floor, frac, frexp, gather, hardswish, hstack, hypot, index_add_, index_copy_, index_put_, index_select, kthvalue, lerp, lgamma, digamma, polygamma, log, log10, log1p, log2, logaddexp, logaddexp2, xlogy, masked_fill_, masked_fill_, masked_scatter_, masked_select, max, maximum, fmax, mean, min, mininum, fmin, mm, mode, mul, lu, lu_solve, vstack}` ([#57768](https://github.com/pytorch/pytorch/pull/57768), [#57863](https://github.com/pytorch/pytorch/pull/57863) [#59711](https://github.com/pytorch/pytorch/pull/59711), [#64742](https://github.com/pytorch/pytorch/pull/64742))
    * Added Forward AD support for the following element-wise and linear operators `torch.{mvlgamma, nan_to_num, permute, pow,  reciprocal, remainder, repeat, round, rsqrt, sigmoid, logit, sign, sgn, sin, sinc, sinh, sqrt, squeeze, sub, sum, t, flip, roll, rot90, take, tan, tanh, trace, transpose, tril, triu, trunc, unfold, unsqueeze, view, zero_, hardshrink} `([#59993](https://github.com/pytorch/pytorch/pull/59993))
    * Added Forward AD support for `torch.special.`{`xlog1py, entr}` ([#59711](https://github.com/pytorch/pytorch/pull/59711), [#59993](https://github.com/pytorch/pytorch/pull/59993))
    * Added forward AD support for `torch.linalg.{cholesky, cholesky_ex, eigh, inv, inv_ex, solve}`  ([#62160](https://github.com/pytorch/pytorch/pull/62160), [#64646](https://github.com/pytorch/pytorch/pull/64646), [#62163](https://github.com/pytorch/pytorch/pull/62163), [#62159](https://github.com/pytorch/pytorch/pull/62159))
    * Added forward AD support for `torch.functional.leak_relu` ([#59993](https://github.com/pytorch/pytorch/pull/59993)) 
* Added saved tensor hooks to customize packing/unpacking behavior of tensors saved for backward ([#60685](https://github.com/pytorch/pytorch/pull/60685), [#60663](https://github.com/pytorch/pytorch/pull/60663), [#62564](https://github.com/pytorch/pytorch/pull/62564), [#60975](https://github.com/pytorch/pytorch/pull/60975), [#62909](https://github.com/pytorch/pytorch/pull/62909), [#62717](https://github.com/pytorch/pytorch/pull/62717))
* Exposed raw saved tensors for custom `autograd.Function` to use with the saved tensor hooks ([#60551](https://github.com/pytorch/pytorch/pull/60551))
* Added default saved tensor hooks ([#61834](https://github.com/pytorch/pytorch/pull/61834), [#62563](https://github.com/pytorch/pytorch/pull/62563), [#62361](https://github.com/pytorch/pytorch/pull/62361))
* Added context manager using default saved tensor hooks to automatically move saved tensors on CPU and back ([#61928](https://github.com/pytorch/pytorch/pull/61928), [#62410](https://github.com/pytorch/pytorch/pull/62410))
* Added C++ and python bindings for `.is_inference()` method ([#58729](https://github.com/pytorch/pytorch/pull/58729)) 
* `torch.lu_solve`: Implement support for backward AD ([#61681](https://github.com/pytorch/pytorch/pull/61681)).

## torch.nn

* Added new modules: `nn.{ReflectionPad3d, LazyInstanceNorm*d}` ([#59791](https://github.com/pytorch/pytorch/pull/59791), [#60837](https://github.com/pytorch/pytorch/pull/60837), [#61308](https://github.com/pytorch/pytorch/pull/61308), [#60982](https://github.com/pytorch/pytorch/pull/60982))
* `nn.CrossEntropyLoss`: Added support for class probability targets ([#61044](https://github.com/pytorch/pytorch/pull/61044))
* `nn.CrossEntropyLoss`: Added support for label smoothing ([#63122](https://github.com/pytorch/pytorch/pull/63122))
* `nn.Module`: Added support for arbitrary objects in state_dicts via `get_extra_state()` / `set_extra_state()` ([#62976](https://github.com/pytorch/pytorch/pull/62976))
* `nn.utils.skip_init()`: Added function to skip module parameter / buffer initialization ([#57555](https://github.com/pytorch/pytorch/pull/57555))

## Profiler

* Added profiler support for mobile ([#62419](https://github.com/pytorch/pytorch/pull/62419), [#62418](https://github.com/pytorch/pytorch/pull/62418), [#62417](https://github.com/pytorch/pytorch/pull/62417),[#62228](https://github.com/pytorch/pytorch/pull/62228),[#62191,](https://github.com/pytorch/pytorch/pull/62191)[#61792](https://github.com/pytorch/pytorch/pull/61792))
* Ported Nvtx support to new profiler ([#61634](https://github.com/pytorch/pytorch/pull/61634))
* Added Tensor core usage stats and recommendations in Tensorboard ([`#364`](https://github.com/pytorch/kineto/pull/364)[,](https://github.com/pytorch/kineto/pull/402/commits/e435a8f55fdbf2a2331931782404b9020eefa4ba)[`#368`](https://github.com/pytorch/kineto/pull/368)[,](https://github.com/pytorch/kineto/pull/402/commits/d3132ebc51faed586e6699e895fecc6b4d255334)[`#383`](https://github.com/pytorch/kineto/pull/383), [`#422`](https://github.com/pytorch/kineto/pull/422))

## CUDA

* Allow enabling warnings on CUDA synchronization ([#62092](https://github.com/pytorch/pytorch/pull/62092))
* Added CUDA graph Prototype API and documentation ([#63269](https://github.com/pytorch/pytorch/pull/63269))
* Make stream semantics of backward calls consistent with other cuda ops ([#57833](https://github.com/pytorch/pytorch/pull/57833), [#60230](https://github.com/pytorch/pytorch/pull/60230), [#60127](https://github.com/pytorch/pytorch/pull/60127))
* Enabled autocast support for user-specified device and dtype ([#61002](https://github.com/pytorch/pytorch/pull/61002), [#63416](https://github.com/pytorch/pytorch/pull/63416))

## C++ API

* Added C++ API for meta functions. They are available in the `at::meta::` namespace ([#58570](https://github.com/pytorch/pytorch/pull/58570))
* Exposed interface to set grain size on `cpu_kernel`, `cpu_kernel_vec` and `cpu_kernel_multiple_outputs` ([#58949](https://github.com/pytorch/pytorch/pull/58949))
* Added `at::native::resize_bytes_cpu` to resize `Storage` in ATen ([#60324](https://github.com/pytorch/pytorch/pull/60324))
* Added `transpose` to PackedTensorAccessor ([#61114](https://github.com/pytorch/pytorch/pull/61114))
* Added `torch::linalg::qr` as the C++ API ([#60529](https://github.com/pytorch/pytorch/pull/60529))
* Exposed `amin` and `amax` to aten symbols ([#61550](https://github.com/pytorch/pytorch/pull/61550))
* Added support to invoke callable activation function for Transformer modules ([#62342](https://github.com/pytorch/pytorch/pull/62342))
* Added support for `c10::optional` to compare with different but comparable types ([#62890](https://github.com/pytorch/pytorch/pull/62890))
* Added a unified API `c10::util::check_env` to check environment variable ([#59052](https://github.com/pytorch/pytorch/pull/59052))

## TorchScript

* Added reference semantics to TorchScript classes ([#44324](https://github.com/pytorch/pytorch/pull/44324)) 
* Conservatively moved all suitable prim ops from full-jit to mobile, and make them selective. ([#58353](https://github.com/pytorch/pytorch/pull/58353)) 
* Added change to predicate uses of RPC APIs on `torch.distributed.rpc.is_available()` ([#58887](https://github.com/pytorch/pytorch/pull/58887)) 
* Added a phase to perform inplace<->functional conversion for activation operators ([#57477](https://github.com/pytorch/pytorch/pull/57477)) 
* Enabled Profile-Directed Typing in `torch.jit.script` ([#62420](https://github.com/pytorch/pytorch/pull/62420)) 
* Introduced enhancement for smart serialization for operator schemas with out arg ([#63096](https://github.com/pytorch/pytorch/pull/63096))
* Added a pass to transform better handle concatenation ops ([#59881](https://github.com/pytorch/pytorch/pull/59881)) 
* Added a new operator for concat that takes in variadic parameters ([#59880](https://github.com/pytorch/pytorch/pull/59880)) 
* Added support for union in TorchScript ([#64234](https://github.com/pytorch/pytorch/pull/64234)) 

## torch.package

* Added basic tooling to enable users to see what is inside of a PackageExporter ([#61147](https://github.com/pytorch/pytorch/pull/61147))
* Added hasattr to `torch::deploy` C++ API ([#62669](https://github.com/pytorch/pytorch/pull/62669))
* Added support to re-save a PackageImporter module ([#65101](https://github.com/pytorch/pytorch/pull/65101))
* Added support to make frozen symbol name customizable in `torch::deploy`. ([#63817](https://github.com/pytorch/pytorch/pull/63817))

## Mobile

* Enabled kineto profiler on mobile via EdgeKinetoProfiler ([#62419](https://github.com/pytorch/pytorch/pull/62419))
* Added support of loading lite interpreter module from assets in Android ([#61609](https://github.com/pytorch/pytorch/pull/61609))
* Enabled tracing based selective build ([#63421,](https://github.com/pytorch/pytorch/pull/63421) [#64087](https://github.com/pytorch/pytorch/pull/64087), [#66237,](https://github.com/pytorch/pytorch/pull/66237) [#66395](https://github.com/pytorch/pytorch/pull/66395))
    * built tracer in OSS  ([#64087](https://github.com/pytorch/pytorch/pull/64087))
    * used operator.yaml to build libtorch library ([#66237)](https://github.com/pytorch/pytorch/pull/66237)
    * Built tracer and enabled tracing-based build with tracer output  ([#66395](https://github.com/pytorch/pytorch/pull/66395))
* NNAPI
    * Android NNAPI delegate implementation of runtime initialization (compilation) and execution ([#62272](https://github.com/pytorch/pytorch/pull/62272))
    * Added `aten::{avgpool2d,softmax,to,div,flatten,detach,slice,log_softmax,conv2d_transpose}` to NNAPI converter ([#58538](https://github.com/pytorch/pytorch/pull/58538), [#58539](https://github.com/pytorch/pytorch/pull/58539), [#58540](https://github.com/pytorch/pytorch/pull/58540), [#58541](https://github.com/pytorch/pytorch/pull/58541), [#60885](https://github.com/pytorch/pytorch/pull/60885), [#58543](https://github.com/pytorch/pytorch/pull/58543), [#59364](https://github.com/pytorch/pytorch/pull/59364), [#61378](https://github.com/pytorch/pytorch/pull/61378), [#59529](https://github.com/pytorch/pytorch/pull/59529)
    * Added Int32 support for NNAPI ([#59365](https://github.com/pytorch/pytorch/pull/59365))
    * Made nnapi `aten::{conv2d,linear,cat,flatten}` converter accept flexible batch ([#61021](https://github.com/pytorch/pytorch/pull/61021), [#61022](https://github.com/pytorch/pytorch/pull/61022), [76c0f223d3](https://github.com/pytorch/pytorch/commit/76c0f223d3), [#61024](https://github.com/pytorch/pytorch/pull/61024))
    * Added option to specify custom NNAPI serializer ([#61025](https://github.com/pytorch/pytorch/pull/61025))
    * Made Android NNAPI preprocess to accept both single Tensor inputs and Tensor List inputs ([#61752](https://github.com/pytorch/pytorch/pull/61752))
    * Added a few improvements in NNAPI delegation ([#63489](https://github.com/pytorch/pytorch/pull/63489))
    * Added support const values in binary ops ([2d58f3f56d](https://github.com/pytorch/pytorch/commit/2d58f3f56d))
* Added unary/binary ops necessary and more shape functions for mobilenet ([#56828](https://github.com/pytorch/pytorch/pull/56828), [#58932](https://github.com/pytorch/pytorch/pull/58932))
* Added `aten::{hardswish,tanh,clamp}` for iOS Metal ([#64588](https://github.com/pytorch/pytorch/pull/64588), [#61383](https://github.com/pytorch/pytorch/pull/61383))
* Added CoreML support ([#64521](https://github.com/pytorch/pytorch/pull/64521), [#64522](https://github.com/pytorch/pytorch/pull/64522), [#64523](https://github.com/pytorch/pytorch/pull/64523))
* Added compatibility API ([#61477](https://github.com/pytorch/pytorch/pull/61477), [#57501](https://github.com/pytorch/pytorch/pull/57501))
* Added support operators with default argument in front of out argument ([#63651](https://github.com/pytorch/pytorch/pull/63651), [#63540](https://github.com/pytorch/pytorch/pull/63540))

## Distributed

`DistributedDataParallel`

* Local SGD and variants for DDP communication optimization ([#60303](https://github.com/pytorch/pytorch/pull/60303), [#60320](https://github.com/pytorch/pytorch/pull/60320), [#60632](https://github.com/pytorch/pytorch/pull/60632), [#60891](https://github.com/pytorch/pytorch/pull/60891), [#61206](https://github.com/pytorch/pytorch/pull/61206), [#61207](https://github.com/pytorch/pytorch/pull/61207), [#62105](https://github.com/pytorch/pytorch/pull/62105), [#62111](https://github.com/pytorch/pytorch/pull/62111), [#62131](https://github.com/pytorch/pytorch/pull/62131), [#62132](https://github.com/pytorch/pytorch/pull/62132), [#62392](https://github.com/pytorch/pytorch/pull/62392), [#63277](https://github.com/pytorch/pytorch/pull/63277), [#63340](https://github.com/pytorch/pytorch/pull/63340), [#64885](https://github.com/pytorch/pytorch/pull/64885), [#65197](https://github.com/pytorch/pytorch/pull/65197))
* Provided a noop hook for performance debugging ([#64344](https://github.com/pytorch/pytorch/pull/64344), [#64352](https://github.com/pytorch/pytorch/pull/64352))
* Implemented BF16 allreduce gradient communication hook ([#63260](https://github.com/pytorch/pytorch/pull/63260))
* Allowed retrieval of model parameters in communication hook ([#61637](https://github.com/pytorch/pytorch/pull/61637))

`torch.distributed`

* Added a function to create new subgroups of a given size ([#59111](https://github.com/pytorch/pytorch/pull/59111))
* Introduced a new torchrun entry point for elastic ([#64049](https://github.com/pytorch/pytorch/pull/64049))

## torch.fx

* Added APIs to mutate specific args/kwargs ([#58571](https://github.com/pytorch/pytorch/pull/58571))
* Introduced EngineHolder for serializing and running TRT Engines with PyTorch ([06399d441d](https://github.com/pytorch/pytorch/commit/06399d441d))
* Introduced `__fx_create_arg__` dunder method for controlling custom classes are handled as node args ([#61780](https://github.com/pytorch/pytorch/pull/61780))
* Added `autowrap_functions` kwarg to Tracer ([#62106](https://github.com/pytorch/pytorch/pull/62106))
* Gradual typing
    * Added type annotation field to nodes ([#60621](https://github.com/pytorch/pytorch/pull/60621))
    * Added experimental gradual typechecker ([#60805](https://github.com/pytorch/pytorch/pull/60805))
    * Extended all experimental type-checking operations to support `conv2d`, `BatchNorm2D`,  `ReLU`, `maxpool2D`, `AdaptiveAvgPooling2D`, `flatten` ([#61093](https://github.com/pytorch/pytorch/pull/61093), [#61012](https://github.com/pytorch/pytorch/pull/61012), [#61150](https://github.com/pytorch/pytorch/pull/61150), [#61188](https://github.com/pytorch/pytorch/pull/61188), [#61239](https://github.com/pytorch/pytorch/pull/61239), [#61265](https://github.com/pytorch/pytorch/pull/61265))
    * Added experimental refinement types and unification for symbolic shape inference ([#61776](https://github.com/pytorch/pytorch/pull/61776))
    * Changed output node handling for typechecker to deal with tuples ([#62582](https://github.com/pytorch/pytorch/pull/62582))
    * Added handle of `get_attr` operations in typechecker ([#62682](https://github.com/pytorch/pytorch/pull/62682))
    * Added equality constraints for some acc operations for symbolic inference ([#63689](https://github.com/pytorch/pytorch/pull/63689))
    * Added inference for algebraic expressions ([#63822](https://github.com/pytorch/pytorch/pull/63822))
* Provided function interface for `remove_duplicate_output_args` ([#65134](https://github.com/pytorch/pytorch/pull/65134))
* Introduced helper function to generate an unique name for an attr in a module ([#64970](https://github.com/pytorch/pytorch/pull/64970))

## ONNX

* Added support for ONNX op set 14 ([#59486](https://github.com/pytorch/pytorch/pull/59486))
* Added support for GRU RNNs with packed input in scripting mode ([#58691](https://github.com/pytorch/pytorch/pull/58691))
* Enhanced shape inference ([#64585](https://github.com/pytorch/pytorch/pull/64585))
* Added support for `torch.{linspace, new_ones, nn.LSTMCell, bernoulli, dot, nn.utils.spectral_norm,bernoulli, distributions.normal.Normal, roll}` ([#58854](https://github.com/pytorch/pytorch/pull/58854), [#59255](https://github.com/pytorch/pytorch/pull/59255), [#62757](https://github.com/pytorch/pytorch/pull/62757), [#62765](https://github.com/pytorch/pytorch/pull/62765), [#59536,](https://github.com/pytorch/pytorch/pull/59536)[#61560,](https://github.com/pytorch/pytorch/pull/61560)[#58697](https://github.com/pytorch/pytorch/pull/58697))

## Infra (Releng)

* Default Linux/Windows testing workflows were migrated to GitHub Actions. PyTorch Probot has been extended to support new set of rerun command with new set of labels that one can use to opt in and opt out of certain types of CI. More information can be found on [Continuous Integration](https://github.com/pytorch/pytorch/wiki/Continuous-Integration#user-guide) wiki page
* Overall statistics and health of PyTorch CI/CD system can be viewed at [https://metrics.pytorch.org](https://metrics.pytorch.org/) ([#65157](https://github.com/pytorch/pytorch/pull/65157), [#61389](https://github.com/pytorch/pytorch/pull/61389), [#62217](https://github.com/pytorch/pytorch/pull/62217), [#64948](https://github.com/pytorch/pytorch/pull/64948), [#60026](https://github.com/pytorch/pytorch/pull/60026), [#61071](https://github.com/pytorch/pytorch/pull/61071), [#64303](https://github.com/pytorch/pytorch/pull/64303))
* Improved mechanism for disabling tests via issues. Creating an issue which title begins with “DISABLED” followed by the test name will disable the test in question for all platforms, which could be refined by explicitly specifying list of platforms in the issue body. Comment from @pytorch-probot would indicate that issue format was recognized by the CI system and test is now disabled. Closing the issue re-enabled the specified test in CI. Disabled tests will be temporarily re-enabled while running CI for PR marked as fixing it ([#61427](https://github.com/pytorch/pytorch/pull/61427))
* New documentation preview and new artifacts frontend. Using [https://hud.pytorch.org](https://hud.pytorch.org/), one can get an overview of PR/commit CI status, download build artifacts as well as read documentation associated with this build. See [Using HUD](https://github.com/pytorch/pytorch/wiki/Using-hud.pytorch.org) wiki page for more information ([#60711](https://github.com/pytorch/pytorch/pull/60711),  [#60792](https://github.com/pytorch/pytorch/pull/60792), [#60893](https://github.com/pytorch/pytorch/pull/60893))

## Misc

* Added support for `torch.fft.` operators on ARM-based platforms using pocket FFT ([#60976](https://github.com/pytorch/pytorch/pull/60976), [#62222](https://github.com/pytorch/pytorch/pull/62222), [#63714](https://github.com/pytorch/pytorch/pull/63714))
* `torch.einsum`: added support for the “sublist” format ([#56625](https://github.com/pytorch/pytorch/pull/56625))
* `torch.linalg.det`: added support for complex autograd ([#58195](https://github.com/pytorch/pytorch/pull/58195))
* Added autograd support for `Tensor.to_sparse` ([#58413](https://github.com/pytorch/pytorch/pull/58413))
* Added more CUDA support for CSR layout: constructors ([#59010](https://github.com/pytorch/pytorch/pull/59010)), sparse_to_dense/add_sparse_csr ([#59011](https://github.com/pytorch/pytorch/pull/59011)), addmm/matvec ([#59012](https://github.com/pytorch/pytorch/pull/59012))
* Vulkan: Added support for `max_pool2d`, `tanh`, `hardshrink`, `log_softmax`, `leaky_relu`, `softmax` ([#58806](https://github.com/pytorch/pytorch/pull/58806), [#60695](https://github.com/pytorch/pytorch/pull/60695), [#62870](https://github.com/pytorch/pytorch/pull/62870), [#63193](https://github.com/pytorch/pytorch/pull/63193), [#62239](https://github.com/pytorch/pytorch/pull/62239))
* Enabled local run of clang-tidy and clang-format lint workflows ([#61121](https://github.com/pytorch/pytorch/pull/61121), [#61797](https://github.com/pytorch/pytorch/pull/61797), [#60745](https://github.com/pytorch/pytorch/pull/60745))

# Improvements

## Python API

* Added clearer stack trace for `torch.floor_divide` deprecation warning ([#64034](https://github.com/pytorch/pytorch/pull/64034))
* Use cascade-summation algorithm to improve `torch.nansum` accuracy ([#61082](https://github.com/pytorch/pytorch/pull/61082))
* `torch.i0`: now promote integer inputs to float ([#52735](https://github.com/pytorch/pytorch/pull/52735))
*  `torch.kthvalue:` added change to adjust output dim size for numpy compatibility ([#59214](https://github.com/pytorch/pytorch/pull/59214))
* Added reduce variants for `torch.scatter` operation. ([#57015](https://github.com/pytorch/pytorch/pull/57015))
* Added support for quantized tensors in `torch.testing.assert_close` ([#58926](https://github.com/pytorch/pytorch/pull/58926))
* Improved error message for invalid value input to Distribution methods ([#61056](https://github.com/pytorch/pytorch/pull/61056))
* `torch.isclose` upcast to most precise dtype within their category before the comparison ([#60536](https://github.com/pytorch/pytorch/pull/60536))
* Added change to cast `alpha` to `acc_type` for `torch.add` and `torch.sub` ([#60227](https://github.com/pytorch/pytorch/pull/60227))
* Fixed dimension in the error message for CUDA `torch.cat` shape check and removed unnecessary offending index information ([#64556](https://github.com/pytorch/pytorch/pull/64556)).
* Improved DLPack support ([#57110](https://github.com/pytorch/pytorch/pull/57110)).
* Added change to raise an error when empty index tensor is passed to `torch.gather` ([#65006](https://github.com/pytorch/pytorch/pull/65006)).
* Added change to store `float64` in `tensorboard` instead of `float32` ([#59435](https://github.com/pytorch/pytorch/pull/59435)).
* Added `use_strict_trace` to tensorboard `add_graph` method ([#63120](https://github.com/pytorch/pytorch/pull/63120)).
* Add option to skip GH validation for `torch.hub` ([#62139](https://github.com/pytorch/pytorch/pull/62139))
* Added a new kwarg `output_size` to `tensor.repeat_interleave`([#58881](https://github.com/pytorch/pytorch/pull/58881))
* Add support for `torch.isclose` ([#63571](https://github.com/pytorch/pytorch/pull/63571))
* Make the behavior of `torch.{testting.assert_close,is_close}` consistent with numpy ([#63841](https://github.com/pytorch/pytorch/pull/63841))

## Autograd

* Added warning about memory leak when `.backward()` is called with `create_graph=True` ([#59412](https://github.com/pytorch/pytorch/pull/59412))
* Added warning when accessing `Tensor::grad()` on a non-leaf Tensor in the C++ API ([#59362](https://github.com/pytorch/pytorch/pull/59362))
* Fixed error message formatting in `grad_output` creation for `.backward()` and `autograd.grad()` ([#59532](https://github.com/pytorch/pytorch/pull/59532))
* Added change to raise `NotImplementedError` for forward and backward-mode AD formulas that are not implemented ([#59482](https://github.com/pytorch/pytorch/pull/59482), [#59483](https://github.com/pytorch/pytorch/pull/59483))
* Reduced memory usage for `torch.relu` for common use cases ([#63089](https://github.com/pytorch/pytorch/pull/63089))
* Added support for non-leaf inputs for `autograd.backward()` function `inputs` argument ([#60521](https://github.com/pytorch/pytorch/pull/60521))
* Improved error message when a tensor with `requires_grad=True`  is passed to a non-differentiable function ([#60610](https://github.com/pytorch/pytorch/pull/60610))
* Made `binary_cross_entropy` differentiable w.r.t. `target` ([#59447](https://github.com/pytorch/pytorch/pull/59447))

## torch.nn

* Added support for inputs with no batch dimensions for `nn.{AdaptiveAvgPool*d, AdaptiveMaxPool*d, AvgPool*d, CosineEmbeddingLoss, Dropout, FractionalMaxPool2d, Linear, LPPool1d, MaxPool*d, MaxUnpool*d, NLLLoss, PairwiseDistance, ReflectionPad*d, ReplicationPad*d, TripletMarginLoss, ZeroPad*d}`, most other loss modules, and all activation modules ([#61264](https://github.com/pytorch/pytorch/pull/61264), [#61847](https://github.com/pytorch/pytorch/pull/61847), [#61860](https://github.com/pytorch/pytorch/pull/61860), [#64590](https://github.com/pytorch/pytorch/pull/64590), [#61911](https://github.com/pytorch/pytorch/pull/61911), [#62490](https://github.com/pytorch/pytorch/pull/62490), [#60992](https://github.com/pytorch/pytorch/pull/60992), [#62190](https://github.com/pytorch/pytorch/pull/62190), [#62206](https://github.com/pytorch/pytorch/pull/62206), [#61984](https://github.com/pytorch/pytorch/pull/61984), [#61310](https://github.com/pytorch/pytorch/pull/61310), [#62651](https://github.com/pytorch/pytorch/pull/62651), [#64882](https://github.com/pytorch/pytorch/pull/64882), [#62183](https://github.com/pytorch/pytorch/pull/62183), [#61060](https://github.com/pytorch/pytorch/pull/61060), [#61262](https://github.com/pytorch/pytorch/pull/61262), [#62729](https://github.com/pytorch/pytorch/pull/62729), [#61300](https://github.com/pytorch/pytorch/pull/61300), [#61461](https://github.com/pytorch/pytorch/pull/61461), [#62726](https://github.com/pytorch/pytorch/pull/62726))
* Added support for inputs with 0 batch size for `nn.{AdaptiveAvgPool*d, AdaptiveMaxPool*d, Bilinear, FractionalMaxPool*d, LocalResponseNorm, MaxPool*d, MaxUnpool*d, TransformerDecoder, TransformerDecoderLayer, TransformerEncoder, TransformerEncoderLayer}` ([#62025](https://github.com/pytorch/pytorch/pull/62025), [#62088](https://github.com/pytorch/pytorch/pull/62088), [#47106](https://github.com/pytorch/pytorch/pull/47106), [#62083](https://github.com/pytorch/pytorch/pull/62083), [#62801](https://github.com/pytorch/pytorch/pull/62801), [#64082](https://github.com/pytorch/pytorch/pull/64082), [#62800](https://github.com/pytorch/pytorch/pull/62800))
* Parametrization: Added support for nested parametrizations, parametrizations depending on several inputs, resizing of parametrized tensors, and the orthogonal parametrization ([#65167](https://github.com/pytorch/pytorch/pull/65167), [#60530](https://github.com/pytorch/pytorch/pull/60530), [#60418](https://github.com/pytorch/pytorch/pull/60418), [#62089](https://github.com/pytorch/pytorch/pull/62089))
* `nn.AvgPool2d`: Added `channels_last` support on CPU ([#58725](https://github.com/pytorch/pytorch/pull/58725))
* `nn.BatchNorm`: Use `resize_output` and `empty` instead of `empty_like` to improve flexibility in output memory format choice ([#63084](https://github.com/pytorch/pytorch/pull/63084))
* `nn.Bilinear`: Added support for non-contiguous tensor inputs ([#38409](https://github.com/pytorch/pytorch/pull/38409))
* `nn.GELU`: Added support for fp32/bfloat16 in CPU path using mkldnn implementation ([#58525](https://github.com/pytorch/pytorch/pull/58525))
* `nn.GroupNorm`: Improved numerical stability by using the Welford algorithm and cascade summation ([#54921](https://github.com/pytorch/pytorch/pull/54921))
* `nn.LayerNorm`: Improved numerical stability by using the Welford algorithm and pairwise sums ([#59987](https://github.com/pytorch/pytorch/pull/59987))
* `nn.NLLLoss`: Added support for target of dtype `byte` ([#60308](https://github.com/pytorch/pytorch/pull/60308), [#60650](https://github.com/pytorch/pytorch/pull/60650))
* `nn.SmoothL1Loss`: Added support for integral target within the backward pass ([#61112](https://github.com/pytorch/pytorch/pull/61112))
* `nn.Transformer`: Added configurable pre/post LayerNorm placement ([#60593](https://github.com/pytorch/pytorch/pull/60593), [#61692](https://github.com/pytorch/pytorch/pull/61692))
* Added check to verify non-zero sequence length for `nn.{RNN, LSTM, GRU}` ([#60269](https://github.com/pytorch/pytorch/pull/60269))
* Added support for bfloat16 in CPU path to `nn.{LeakyReLU, RReLU}` ([#61514](https://github.com/pytorch/pytorch/pull/61514))
* Added support for `channels_last` memory format in `nn.{AdaptiveMaxPool2d, GroupNorm}` ([#48920](https://github.com/pytorch/pytorch/pull/48920), [#49821](https://github.com/pytorch/pytorch/pull/49821))
* Added callable activation function support to `nn.{MultiheadAttention, Transformer, TransformerDecoderLayer, TransformerEncoderLayer}` ([#61355](https://github.com/pytorch/pytorch/pull/61355), [#62342](https://github.com/pytorch/pytorch/pull/62342))

## Profiler

* Changed `profiler.profile` argument `with_flops`  when set to `True` to report total FLOPs rather than FLOP/s, and support more operators ([#62779](https://github.com/pytorch/pytorch/pull/62779), [#61895](https://github.com/pytorch/pytorch/pull/61895))
* Improved memory profiling and Tensorboard memory view, enabling better understanding of memory usage by showing active memory allocations at various points of your program run as well as a memory usage trend chart.  ([#61282](https://github.com/pytorch/pytorch/pull/61282), [`#361`](https://github.com/pytorch/kineto/pull/361), [`#404`](https://github.com/pytorch/kineto/pull/404)[,](https://github.com/pytorch/kineto/pull/435/commits/36f069ad8f819255f5b575782e99b0c4573a6d0f)[`#416`](https://github.com/pytorch/kineto/pull/416)[,](https://github.com/pytorch/kineto/pull/435/commits/d6d28b719270b1ceb10fca1003cfb77a11e18c79)[`#421`](https://github.com/pytorch/kineto/pull/421))
* Added flow arrows between ops in the forward pass and the corresponding ops in the backward pass in the trace view ([#62553](https://github.com/pytorch/pytorch/pull/62553), [#372](https://github.com/pytorch/kineto/pull/372))
* Increased profiling coverage of backward pass ([#63619](https://github.com/pytorch/pytorch/pull/63619))
* Made threads and GPU streams appear in a consistent sorted order in the trace view ([#399](https://github.com/pytorch/kineto/pull/399))
* Added shapes and reg usage to the GPU kernel view ([`#351`](https://github.com/pytorch/kineto/pull/351)[)](https://github.com/pytorch/kineto/pull/402/commits/eed895ba7ce521deb457dee4678d7a6c8a4a7bd6)

## Dataloader

* Properly delegated indices called by `Subset` to dataset ([#59513](https://github.com/pytorch/pytorch/pull/59513))
* Removed the restriction that input datasets in `ConcatDataset` must be `Sized` ([#64114](https://github.com/pytorch/pytorch/pull/64114))
* Allowed annotation of `IterableDataset` to accept keyword-only arguments and `abc` class ([#58450](https://github.com/pytorch/pytorch/pull/58450))
* Changed annotation of `DataLoader` to accept non-integer `Sampler` as input([#63500](https://github.com/pytorch/pytorch/pull/63500))

## CUDA

* Include function name in the error message for inputs being on different devices ([#58502](https://github.com/pytorch/pytorch/pull/58502))
* Fix MAGMA initialization ([#58521](https://github.com/pytorch/pytorch/pull/58521))
* Updated NCCL to 2.10 ([#62276](https://github.com/pytorch/pytorch/pull/62276))
* Added deterministic path for `torch.scatter_add` for 1D tensors ([#58761](https://github.com/pytorch/pytorch/pull/58761))
* Added CUDA support for mean reduction ([#59543](https://github.com/pytorch/pytorch/pull/59543))
* Add missing CUDA kernel launch check ([#60114](https://github.com/pytorch/pytorch/pull/60114))
* Improved CUDA extension building error/warning messages ([#59665](https://github.com/pytorch/pytorch/pull/59665), [#60592](https://github.com/pytorch/pytorch/pull/60592))
* Added change to compute CUDA reduction buffer size in elements ([#63969](https://github.com/pytorch/pytorch/pull/63969))

## TorchScript

* Added change to simplify pass on arithmetic expressions for integers. ([#61444](https://github.com/pytorch/pytorch/pull/61444)) 
* Set future's error to current exception as is when `--torch_jit_enable_rethrow_caught_exception=true` ([#63348](https://github.com/pytorch/pytorch/pull/63348)) 
* Improved TorchScript module getattr() to be same as python class getattr() method ([#61599](https://github.com/pytorch/pytorch/pull/61599)) 
* Improved slicing for scripted version of `torch.nn.ModuleList` to support arbitrary step size ([#58361](https://github.com/pytorch/pytorch/pull/58361)) 
* Added parsing logic for `Tuple[()]` annotation ([#58340](https://github.com/pytorch/pytorch/pull/58340)) 
* Changed list striding kernel implementation to handle optional integers ([#58536](https://github.com/pytorch/pytorch/pull/58536)) 
* Added support for `torch.nn.Parameter` type for Profile-Directed-Typing ([#59249](https://github.com/pytorch/pytorch/pull/59249)) 
* Added change to annotate NoneType as Optional[type] ([#60383](https://github.com/pytorch/pytorch/pull/60383)) 
* Added support for default values on NamedTuple fields ([#54682](https://github.com/pytorch/pytorch/pull/54682)) 
* Improved JIT support for `torch.einsum` ([#59265](https://github.com/pytorch/pytorch/pull/59265)) 
* Added change to allow for heterogenous List and Dict values + Improve container typing algorithm ([#57137](https://github.com/pytorch/pytorch/pull/57137)) 
* Added support for eager mode use of `torch.jit.isinstance` with multiple types ([#60465](https://github.com/pytorch/pytorch/pull/60465)) 
* Allowed uncompiled strings as input to `checkScriptRaisesRegex` ([#63901](https://github.com/pytorch/pytorch/pull/63901))
* Introduced more robust check of whether a class is defined in torch ([#64083](https://github.com/pytorch/pytorch/pull/64083)) 
* Added change to preserve types during empty container assignment ([#58911](https://github.com/pytorch/pytorch/pull/58911)) 
* Made JIT not assume that the device is CUDA. ([#54238](https://github.com/pytorch/pytorch/pull/54238)) 
* Updated `optimize_for_mobile` to preserve nodes’ debug information ([#63106](https://github.com/pytorch/pytorch/pull/63106)) 
* Added support for device as Dict key ([#65079](https://github.com/pytorch/pytorch/pull/65079))  
* Added support for Python C extension modules in `torch::deploy` ([#58117](https://github.com/pytorch/pytorch/pull/58117)) 
* Added a flag to suppress stacktrace in exception messages([#63073](https://github.com/pytorch/pytorch/pull/63073)) 
* Added API to change logging levels for JIT ([#58821](https://github.com/pytorch/pytorch/pull/58821)) 
* Provided API to preserve source range and callstack information during graph rewrite ([#58300](https://github.com/pytorch/pytorch/pull/58300)) 
* Re-enabled BatchNorm autodiff  ([#57321](https://github.com/pytorch/pytorch/pull/57321)) 
* Extracted element-wise ops supported by JIT fuser into a separate list ([#59579](https://github.com/pytorch/pytorch/pull/59579)) 
* Reworked requires_grad on DifferentiableGraphOp ([#57575](https://github.com/pytorch/pytorch/pull/57575)) 

## torch.package

* Unified three categories of dependency handling error (broken, denied, unhandled) into a single "error" field in the node, with optional context ([#58572](https://github.com/pytorch/pytorch/pull/58572))
* Renamed MockZipReader into DirectoryReader ([#59107](https://github.com/pytorch/pytorch/pull/59107))
* Added change to silently skip cases where the __**import__** statement cannot be parsed ([#61148](https://github.com/pytorch/pytorch/pull/61148))
* Make torch::deploy work with or without cuda ([#58493](https://github.com/pytorch/pytorch/pull/58493))

## Mobile

* Added check to ensure op name does not contain open parenthesis ([#58687](https://github.com/pytorch/pytorch/pull/58687))
* Added handles and symbolicate exception callstack thrown from backend ([#55462](https://github.com/pytorch/pytorch/pull/55462), [#57441](https://github.com/pytorch/pytorch/pull/57441), [#57481](https://github.com/pytorch/pytorch/pull/57481))
* Enabled implicit operator versioning via number of arguments ([#58852](https://github.com/pytorch/pytorch/pull/58852))
* Cleaned up unused APIs and improve debugging experience for iOS GPU ([#60280](https://github.com/pytorch/pytorch/pull/60280), [#60281,](https://github.com/pytorch/pytorch/pull/60281)[#60282](https://github.com/pytorch/pytorch/pull/60282))
* Added debug information to track memory allocation exception for Metal ([#59112](https://github.com/pytorch/pytorch/pull/59112))
* Added print of IValue type name in error message for Android ([#64602](https://github.com/pytorch/pytorch/pull/64602))
* Added print of error message when failing to load model file ([#63404](https://github.com/pytorch/pytorch/pull/63404))
* Introduced multiple improvements in `torch.utils.model_dump` APIs: 
    * Make stdout argument for main kwarg-only ([#60699](https://github.com/pytorch/pytorch/pull/60699))
    * Implement "Hider" properly ([#57654](https://github.com/pytorch/pytorch/pull/57654))
    * Handle `torch.device` objects ([#57656](https://github.com/pytorch/pytorch/pull/57656))
    * Handle dict rendering ([#57657](https://github.com/pytorch/pytorch/pull/57657))
    * Add a section that summarizes tensor memory usage ([#57658](https://github.com/pytorch/pytorch/pull/57658))
    * Handle invalid UTF-8 in pickles ([#57661](https://github.com/pytorch/pytorch/pull/57661))

## Quantization

* Added out variant for int8 `quantized::linear` ([#58282](https://github.com/pytorch/pytorch/pull/58282)) and `quantized::embedding_bag_byte_prepack` ([#64081](https://github.com/pytorch/pytorch/pull/64081))
* FX graph mode quantization: improve `qconfig_dict` argument handling ([#59605](https://github.com/pytorch/pytorch/pull/59605), [#58566](https://github.com/pytorch/pytorch/pull/58566))
* Added support to embedding trained in FP16 ([#60736](https://github.com/pytorch/pytorch/pull/60736))
* Added support for `torch.index_select` on quantized tensors ([#61406](https://github.com/pytorch/pytorch/pull/61406))
* Added a new fused MovingAvg Obs + FakeQuant operator ([#61570](https://github.com/pytorch/pytorch/pull/61570), [#61589](https://github.com/pytorch/pytorch/pull/61589), [#61691](https://github.com/pytorch/pytorch/pull/61691), [#62346](https://github.com/pytorch/pytorch/pull/62346), [#62863](https://github.com/pytorch/pytorch/pull/62863), [#62702](https://github.com/pytorch/pytorch/pull/62702), [#63043](https://github.com/pytorch/pytorch/pull/63043), [#64829](https://github.com/pytorch/pytorch/pull/64829))
* Added support for dynamic linear + relu fusion (INT8) ([#63799](https://github.com/pytorch/pytorch/pull/63799),[#63826](https://github.com/pytorch/pytorch/pull/63826))
* Enabled JIT tracing on quantizable LSTM ([#64438](https://github.com/pytorch/pytorch/pull/64438))

## Distributed

`DistributedDataParallel`

* Added error logging to DDP logging API ([#59281](https://github.com/pytorch/pytorch/pull/59281), [#59284](https://github.com/pytorch/pytorch/pull/59284), [#59351,](https://github.com/pytorch/pytorch/pull/59351)[#65023](https://github.com/pytorch/pytorch/pull/65023))
* Added `NCCL_ASYNC_ERROR_HANDLING` environment variable to control NCCL error handling ([#59109](https://github.com/pytorch/pytorch/pull/59109))
* Communication hook APIs to always return single tensor ([#62074](https://github.com/pytorch/pytorch/pull/62074), [#62389](https://github.com/pytorch/pytorch/pull/62389), [#62457](https://github.com/pytorch/pytorch/pull/62457))
* Added DDP bucket sizes in DDP logging API ([#62229](https://github.com/pytorch/pytorch/pull/62229), [#62232](https://github.com/pytorch/pytorch/pull/62232), [#62231](https://github.com/pytorch/pytorch/pull/62231), [#62625](https://github.com/pytorch/pytorch/pull/62625), 
* Improved rebuilding buckets logic  ([#62279](https://github.com/pytorch/pytorch/pull/62279), [#58097](https://github.com/pytorch/pytorch/pull/58097))
* Allowed DDP uneven inputs work with communication hooks ([#61017](https://github.com/pytorch/pytorch/pull/61017), [#61018](https://github.com/pytorch/pytorch/pull/61018), [#61019](https://github.com/pytorch/pytorch/pull/61019), [#61020](https://github.com/pytorch/pytorch/pull/61020))
* Added logging if graph is static at end of training ([#61871](https://github.com/pytorch/pytorch/pull/61871))
* Added logging of unused param names under DETAIL debug mode. ([#62209](https://github.com/pytorch/pytorch/pull/62209))
* Allowed tuning of first bucket in DDP ([#62748](https://github.com/pytorch/pytorch/pull/62748))
* Added gradient ready order, host-side timestamps, and bucket indices to DDP logging ([#62751](https://github.com/pytorch/pytorch/pull/62751), [#62770](https://github.com/pytorch/pytorch/pull/62770))
* Added a debug check in C++ fp16 gradient hook ([#63379](https://github.com/pytorch/pytorch/pull/63379))
* Added a fallback to use `mul` and `copy_` instead of `mul`’s `out=` variant when gradient tensor requires grad in DDP ([#63831](https://github.com/pytorch/pytorch/pull/63831))
* Used `Tensor.set_` instead of directory assigning data in model averaging ([#63895](https://github.com/pytorch/pytorch/pull/63895))
* Added more iterations for DDP logging ([#64071](https://github.com/pytorch/pytorch/pull/64071),  [#64411](https://github.com/pytorch/pytorch/pull/64411))

`torch.distributed`

* Introduced ProcessGroup wrapper and use it in debug mode([#58224](https://github.com/pytorch/pytorch/pull/58224), [#58281](https://github.com/pytorch/pytorch/pull/58281), [#60237](https://github.com/pytorch/pytorch/pull/60237))
* Made a small change for `torch.distributed` launcher ([#59152](https://github.com/pytorch/pytorch/pull/59152))
* Added complex number support for all_to_all/scatter ([#61299](https://github.com/pytorch/pytorch/pull/61299))
* Made gloo communication profiling more accurate ([#61342](https://github.com/pytorch/pytorch/pull/61342))
* Used generator instead of list to save memory in scatter ([#62516](https://github.com/pytorch/pytorch/pull/62516))
* Provided failure reason from ProcessGroup when aborting NCCL communicator ([#64241](https://github.com/pytorch/pytorch/pull/64241))
* Introduced error raised when capturing uncapturable NCCL in CUDA graphs. ([#64440](https://github.com/pytorch/pytorch/pull/64440))
* Added Single-Machine Model Parallel Support to `torch.distributed.optim.ZeroRedundancyOptimizer` ([#61370](https://github.com/pytorch/pytorch/pull/61370))

`torch.distributed.nn.RemoteModule`

* Supported creating a RemoteModule by RRef ([#59242](https://github.com/pytorch/pytorch/pull/59242))
* Supported switching RemoteModule between train/eval ([#59026](https://github.com/pytorch/pytorch/pull/59026))

`torch.distributed.elastic`

* Added minor logging and error formatting improvements ([#63214](https://github.com/pytorch/pytorch/pull/63214),  [#62823](https://github.com/pytorch/pytorch/pull/62823))
* Improved process termination logic ([#61602](https://github.com/pytorch/pytorch/pull/61602))
* Added fqdn hostname to error printout ([#66662](https://github.com/pytorch/pytorch/pull/66662/))

`torch.distributed.rpc`

* Fix RPC initialization to avoid shutdown timeout ([#59801](https://github.com/pytorch/pytorch/pull/59801))
* Supported RRefs that contain `threading.Locks` ([#57943](https://github.com/pytorch/pytorch/pull/57943)), `torch.cuda.Event` ([#61354](https://github.com/pytorch/pytorch/pull/61354))
* Updated rpc tensorpipe logic for sparse tensors ([#64575](https://github.com/pytorch/pytorch/pull/64575))
* Added rpc sparse tensor fix ([#59609](https://github.com/pytorch/pytorch/pull/59609), [#62794](https://github.com/pytorch/pytorch/pull/62794))
* Added change to ensure that future completion doesn't swallow exception. ([#61094](https://github.com/pytorch/pytorch/pull/61094))
* Set streams when invoking UDFs ([#59210](https://github.com/pytorch/pytorch/pull/59210))
* Set and propagate devices in RRef completion Future ([#59211](https://github.com/pytorch/pytorch/pull/59211))
* Made TensorPipe agent use streams from Future when sending response ([#59212](https://github.com/pytorch/pytorch/pull/59212))
* Added change to leverage TensorPipe's automatic SHM address selection ([#63028](https://github.com/pytorch/pytorch/pull/63028))
* Made Future store Storages instead of references to DataPtrs ([#60470](https://github.com/pytorch/pytorch/pull/60470), [#60943](https://github.com/pytorch/pytorch/pull/60943))
* Added change to avoid re-doing CUDA stream sync in OwnerRRef ([#57355](https://github.com/pytorch/pytorch/pull/57355))

`torch.distributed.Store`

* Enhanced connect timeout error message ([#61390](https://github.com/pytorch/pytorch/pull/61390))
* Added minor fixes in c10d for Windows ([#62953](https://github.com/pytorch/pytorch/pull/62953))

`torch.distributed.pipeline`

* Supported non-tensor inputs in pipeline parallel API ([#55441](https://github.com/pytorch/pytorch/pull/55441), [#57226](https://github.com/pytorch/pytorch/pull/57226), [#57325](https://github.com/pytorch/pytorch/pull/57325))
* Added a `WithDevice` wrapper to specify device execution for a module. ([#65190](https://github.com/pytorch/pytorch/pull/65190))

## torch.fx

* Added users of a node to the serialized JSON ([#59357](https://github.com/pytorch/pytorch/pull/59357))
* Added requires_grad to TensorMetadata ([#60972](https://github.com/pytorch/pytorch/pull/60972))
* Added change to swap out Python's AnnAssign with an Assign node where the annotation function is called ([#60622](https://github.com/pytorch/pytorch/pull/60622))
* Added type annotations for the `torch.nn.Module` constructor ([#61334](https://github.com/pytorch/pytorch/pull/61334))
* Enabled `torch.deploy` for GraphModules with non-torch dependencies ([#61680](https://github.com/pytorch/pytorch/pull/61680))
* Added change to allow FX tracer to trace control flow (if/while) statements when parameter shapes are in the conditionals ([#61820](https://github.com/pytorch/pytorch/pull/61820))
* Added `torch.memory_format` as a BaseArgumentType ([#62593](https://github.com/pytorch/pytorch/pull/62593))
* Added backwards compatibility guarantees for 1.10 ([#63888](https://github.com/pytorch/pytorch/pull/63888))
    * Renamed reduce functions back to their old, public names ([#64324](https://github.com/pytorch/pytorch/pull/64324))
    * Added change to ensure BC coverage for all of `torch.fx` passes ([#65081](https://github.com/pytorch/pytorch/pull/65081))
* Add `__matmul__` to the magic methods for FX tracing ([#64512](https://github.com/pytorch/pytorch/pull/64512))

## Composability

* Added meta tensor support for `torch.{any, all, fmax, fmin, remainder, glu, argmax, argmin, avg_pool3d_backward, isposinf, isneginf, fmod, fmin, signbit, slow_conv_transpose2d, nll_loss_backward, cumprod, aminmax, addcmul, addcdiv, gather, hardshrink_backward, softshrink_backward, hardshrink, gelu, gelu_backward, avg_pool2d, avg_pool2d_backward, avg_pool3d, reflection_pad1d_backward, all, any, silu_backward, sgn, softplus, leaky_relu_backward, hardsigmoid_backward, elu_backward, eq, xlogy, ne, lt, gt, le, ge, sigmoid_backward, tanh_backward, logit_backward, bitwise_or, bitwise_xor, bitwise_and, nll_loss_forward, log_softmax, log_softmax_backward_data, prod, norm, sum.dim_IntList, clamp}` ([#64642](https://github.com/pytorch/pytorch/pull/64642), [#58458,](https://github.com/pytorch/pytorch/pull/58458)[#58732](https://github.com/pytorch/pytorch/pull/58732), [#61800](https://github.com/pytorch/pytorch/pull/61800), [#60363](https://github.com/pytorch/pytorch/pull/60363), [#60364](https://github.com/pytorch/pytorch/pull/60364), [#59084](https://github.com/pytorch/pytorch/pull/59084), [#60633](https://github.com/pytorch/pytorch/pull/60633), [#60809](https://github.com/pytorch/pytorch/pull/60809), [#60810](https://github.com/pytorch/pytorch/pull/60810), [#57936](https://github.com/pytorch/pytorch/pull/57936), [#55503](https://github.com/pytorch/pytorch/pull/55503), [#62144](https://github.com/pytorch/pytorch/pull/62144), [#61899](https://github.com/pytorch/pytorch/pull/61899), [#62401](https://github.com/pytorch/pytorch/pull/62401), [#62318](https://github.com/pytorch/pytorch/pull/62318), [#62319](https://github.com/pytorch/pytorch/pull/62319), [#63312](https://github.com/pytorch/pytorch/pull/63312), [#58662](https://github.com/pytorch/pytorch/pull/58662), [#58663](https://github.com/pytorch/pytorch/pull/58663), [#58664](https://github.com/pytorch/pytorch/pull/58664), [#58665](https://github.com/pytorch/pytorch/pull/58665), [#58987](https://github.com/pytorch/pytorch/pull/58987), [#59082](https://github.com/pytorch/pytorch/pull/59082), [#59083](https://github.com/pytorch/pytorch/pull/59083), [#59103](https://github.com/pytorch/pytorch/pull/59103), [#60360](https://github.com/pytorch/pytorch/pull/60360), [#60361](https://github.com/pytorch/pytorch/pull/60361), [#58661](https://github.com/pytorch/pytorch/pull/58661), [#58197](https://github.com/pytorch/pytorch/pull/58197), [#58482](https://github.com/pytorch/pytorch/pull/58482), [#58483](https://github.com/pytorch/pytorch/pull/58483), [#58484](https://github.com/pytorch/pytorch/pull/58484), [#58660](https://github.com/pytorch/pytorch/pull/58660), [#60177](https://github.com/pytorch/pytorch/pull/60177), [#60814](https://github.com/pytorch/pytorch/pull/60814), [#60942](https://github.com/pytorch/pytorch/pull/60942), [#60815](https://github.com/pytorch/pytorch/pull/60815), [#60816](https://github.com/pytorch/pytorch/pull/60816), [#60817](https://github.com/pytorch/pytorch/pull/60817), [#60811](https://github.com/pytorch/pytorch/pull/60811), [#60812](https://github.com/pytorch/pytorch/pull/60812), [#60813](https://github.com/pytorch/pytorch/pull/60813), [#61443](https://github.com/pytorch/pytorch/pull/61443), [#57374](https://github.com/pytorch/pytorch/pull/57374), [#62372](https://github.com/pytorch/pytorch/pull/62372), [#62024](https://github.com/pytorch/pytorch/pull/62024), [#62711](https://github.com/pytorch/pytorch/pull/62711), [#61642](https://github.com/pytorch/pytorch/pull/61642), [#61361](https://github.com/pytorch/pytorch/pull/61361))
* PyObject preservation: Previously, tensors in python that no longer had any python-side references (but still had references in C++, e.g. if it’s saved for autograd) would get deallocated, and we would create a new Python object to replace it next time it passes from C++ to Python. We now preserve the PyObject as long as there are any references on either the python or C++ side. This ensures that any metadata on the original python object is preserved. For example, tensor subclasses that were saved for autograd now get properly preserved. ([#56017](https://github.com/pytorch/pytorch/pull/56017))

## Build_Frontend

* Added a new include directory in BLIS search path ([#58166](https://github.com/pytorch/pytorch/pull/58166))
* Added print to show full Python version in `torch.utils.collect_env` ([#59632](https://github.com/pytorch/pytorch/pull/59632))
* Added change to respect `CMAKE_PREFIX_PATH` choice set by caller ([#61904](https://github.com/pytorch/pytorch/pull/61904))
* Dropped incremental linking on Windows when REL_WITH_DEB_INFO=1. ([#64892](https://github.com/pytorch/pytorch/pull/64892))
* Enabled kineto build for ROCm platform ([#58401](https://github.com/pytorch/pytorch/pull/58401))
* Added support to system-provided Intel TBB ([#61934](https://github.com/pytorch/pytorch/pull/61934))
* Added Pytorch build support with [Newlib](https://en.wikipedia.org/wiki/Newlib) c library ([#60345](https://github.com/pytorch/pytorch/pull/60345), [#60052](https://github.com/pytorch/pytorch/pull/60052))
* Imrpove `torch.__version__` comparisons ([#61556](https://github.com/pytorch/pytorch/pull/61556), [#64565](https://github.com/pytorch/pytorch/pull/64565), [#63848](https://github.com/pytorch/pytorch/pull/63848))
* CMake: added optional precompiled header support ([#61940](https://github.com/pytorch/pytorch/pull/61940))
* Removed unnecessary Ubuntu version checks ([#61738](https://github.com/pytorch/pytorch/pull/61738))
* Added GPU support to `bazel` builds ([#63604](https://github.com/pytorch/pytorch/pull/63604))

## Infra (Releng)

* Improved automated test sharding. ([#59727](https://github.com/pytorch/pytorch/pull/59727), [#60206](https://github.com/pytorch/pytorch/pull/60206))
* Added change to strictly type everything in .github and tools ([#59117](https://github.com/pytorch/pytorch/pull/59117))
* Upgraded Windows CI Python to 3.8 ([#59729](https://github.com/pytorch/pytorch/pull/59729)) and CUDA to 10.2 ([#65080](https://github.com/pytorch/pytorch/pull/65080))
* Made change to use expecttest from PyPI ([#60658](https://github.com/pytorch/pytorch/pull/60658), [#63320](https://github.com/pytorch/pytorch/pull/63320))
* Added option to run specified tests option to run_test.py ([#59649](https://github.com/pytorch/pytorch/pull/59649))
* Enabled Metal in PyTorch MacOS/iOS nightly builds ([#63718](https://github.com/pytorch/pytorch/pull/63718), [#65075](https://github.com/pytorch/pytorch/pull/65075))
* Added retries to flaky CI steps. ([#65013](https://github.com/pytorch/pytorch/pull/65013), [#65104](https://github.com/pytorch/pytorch/pull/65104), [#64120](https://github.com/pytorch/pytorch/pull/64120), [#60216](https://github.com/pytorch/pytorch/pull/60216), [#63319](https://github.com/pytorch/pytorch/pull/63319))
* Allowed Docker build on macOS ([#60375](https://github.com/pytorch/pytorch/pull/60375))

## Misc

* Added support for MIOpen channel last convolution ([#63617](https://github.com/pytorch/pytorch/pull/63617))
* Enabled kernel asserts on rocm ([#49624](https://github.com/pytorch/pytorch/pull/49624))
* Added bool, float16, bfloat16 and complex support for to_dense for CSR sparse Tensors ([#60657](https://github.com/pytorch/pytorch/pull/60657))
* Added complex dtype support for matrix multiplication of two COO sparse Tensors on CPU ([#59554](https://github.com/pytorch/pytorch/pull/59554))
* Added the “upper” kwarg to `torch.linalg.cholesky` ([#62434](https://github.com/pytorch/pytorch/pull/62434))
* Improved error message in ONNX when attempting to export dict modification ([#58696](https://github.com/pytorch/pytorch/pull/58696))
* Migrated `THAllocator` to `MapAllocator` in ATen ([#60325](https://github.com/pytorch/pytorch/pull/60325))
* Converted input type of `TensorOptions.device_index` from `int16_t` to to `c10::DeviceIndex` ([#60412](https://github.com/pytorch/pytorch/pull/60412))

# Bug fixes

## Python API

* Added fix to recognize transposed dense tensors as a form of partial overlap ([#59014](https://github.com/pytorch/pytorch/pull/59014))
* Fixed `torch.polygamma` incorrect behavior at infinites when n>=1 ([#61641](https://github.com/pytorch/pytorch/pull/61641))
* Fixed for non-contiguous inputs for `torch.{sort,topk}` on CUDA ([#63029](https://github.com/pytorch/pytorch/pull/63029)), `torch.tensor_split` indices([#63390](https://github.com/pytorch/pytorch/pull/63390))
* Fixed legacy constructor `torch.Tensor`  when given a scalar Tensor ([#58885](https://github.com/pytorch/pytorch/pull/58885))
* Added change to not wrap `Tensor.{grad,_base}` by default for Tensor-like objects([#60464](https://github.com/pytorch/pytorch/pull/60464))
* Fixed `torch.angle` on aarch64 ([#59832](https://github.com/pytorch/pytorch/pull/59832))
* Fixed specialized convolution kernel on arm64 ([#60460](https://github.com/pytorch/pytorch/pull/60460))
* `torch.normal`: fixed RuntimeError when standard deviation named arg is torch.empty [(#66524](https://github.com/pytorch/pytorch/pull/66524/))
* Fixed random sampling on SGX platforms ([#60368](https://github.com/pytorch/pytorch/pull/60368))
* Fixed testing when Scipy is not available ([#61699](https://github.com/pytorch/pytorch/pull/61699))
* Fixed `torch.Tensor.copy_` when using large inputs and broadcasting ([#64425](https://github.com/pytorch/pytorch/pull/64425))
* Fixed broadcasting behavior for `torch.trapezoid` ([#64054](https://github.com/pytorch/pytorch/pull/64054)).
* Fixed dtype check of comparison ops ([#64267](https://github.com/pytorch/pytorch/pull/64267)).
* Fixed `torch.median` crash on empty tensor ([#61698](https://github.com/pytorch/pytorch/pull/61698))
* Fixed missing lazy initialization in `torch.get_num_threads` ([#64486](https://github.com/pytorch/pytorch/pull/64486))
* Fixed check for empty named dims list to `torch.flatten` ([#61953](https://github.com/pytorch/pytorch/pull/61953))
* Fixed `torch.hub.{list,help}` functions for Windows ([#63773](https://github.com/pytorch/pytorch/pull/63773))
* Fixed `torch.{istft,rfft}` errors for special inputs ([#63469](https://github.com/pytorch/pytorch/pull/63469), [#63327](https://github.com/pytorch/pytorch/pull/63327))
* Fixed type annotation
    * `optim.lr_scheduler.CosineAnnealingWarmRestart` ([#61106](https://github.com/pytorch/pytorch/pull/61106))
    * Fixed type annotation of `torch.hub.load` ([#63755](https://github.com/pytorch/pytorch/pull/63755))
* `x[index] = value` no longer results in a RuntimeError if `x` and `value` are different devices.
    ([#61612](https://github.com/pytorch/pytorch/pull/61612))
* Fixed crash while creating new tensor if NumPy is not available ([#66433](https://github.com/pytorch/pytorch/pull/66433))
* Handle exceptions from THPModule_setQEngine ([#60073](https://github.com/pytorch/pytorch/pull/60073))
* Fixed `torch.Tensor.cauchy_` on CUDA for inf values ([#60186](https://github.com/pytorch/pytorch/pull/60186))

## Autograd

* `torch.{signbit,isin}` no longer raise an error when passed a tensor that requires grad ([#62529](https://github.com/pytorch/pytorch/pull/62529))
* Fixed sub-gradient for `torch.a{max,min}` ([#59669](https://github.com/pytorch/pytorch/pull/59669))
* Fixed segfaults when a tensor hook removes itself ([#61250](https://github.com/pytorch/pytorch/pull/61250))
* Fixed double backward for `binary_cross_entropy` loss function when `reduction=sum`. ([#59479](https://github.com/pytorch/pytorch/pull/59479))
* Made sure that TLS (grad mode, inference mode, dispatcher state, etc) are properly set in hooks being called during the backward pass ([#60067](https://github.com/pytorch/pytorch/pull/60067))

## torch.nn

* `nn.AdaptiveAvgPool2d`: Correctly dispatch to CUDA implementation ([#61851](https://github.com/pytorch/pytorch/pull/61851))
* `nn.AdaptiveAvgPool3d`: Fixed gradient computation ([#60630](https://github.com/pytorch/pytorch/pull/60630))
* `nn.BatchNorm`: Fixed mixed precision usage when `affine=False` ([#61962](https://github.com/pytorch/pytorch/pull/61962))
* `nn.BatchNorm2d`: Fixed issue when input is non-contiguous ([#63392](https://github.com/pytorch/pytorch/pull/63392))
* Fixed `batch_norm()` to preserve output memory layout based on input ([#62773](https://github.com/pytorch/pytorch/pull/62773))
* `nn.MaxPool2d`: Use `channels_last` memory format for output and indices when input is channels_last ([#61245](https://github.com/pytorch/pytorch/pull/61245))
* `nn.Module`: Fixed full backward hook when grad is disabled ([#65335](https://github.com/pytorch/pytorch/pull/65335))
* `nn.Module`: Fixed `get_buffer()` to check buffers by name instead of value ([#61429](https://github.com/pytorch/pytorch/pull/61429))
* `nn.Module`: Fixed pre-forward hooks for Lazy modules ([#60517](https://github.com/pytorch/pytorch/pull/60517))
* `nn.Softmax`: Improve numerical stability by subtracting max value in vectorized CPU implementation ([#63132](https://github.com/pytorch/pytorch/pull/63132))
* `F.cosine_similarity`: Fixed type promotion behavior and added input validation checks ([#62054](https://github.com/pytorch/pytorch/pull/62054), [#66191](https://github.com/pytorch/pytorch/pull/66191), [#62912](https://github.com/pytorch/pytorch/pull/62912), [#58559](https://github.com/pytorch/pytorch/pull/58559))
* `F.embedding`: Added check to validate that weights are 2D ([#59314](https://github.com/pytorch/pytorch/pull/59314))
* `F.interpolate`: Fixed output for edge case of single pixel without align_corners ([#61166](https://github.com/pytorch/pytorch/pull/61166))
* `F.nll_loss`: Fixed regression for gradient computation ([#64203](https://github.com/pytorch/pytorch/pull/64203))
* `F.pad`: Fixed type of default pad value to be floating point ([#62095](https://github.com/pytorch/pytorch/pull/62095))
* Fixed issues with printing `torch._ops.ops.{atan, quantized}` modules ([#62447](https://github.com/pytorch/pytorch/pull/62447))
* Fixed `torch.nn.utils.parametrizations.spectral_norm` so that it can be used twice in the same forward pass ([#62293](https://github.com/pytorch/pytorch/pull/62293))
* Disabled cuDNN persistent RNN on A30 to avoid exceptions from hard-to-detect edge cases ([#59830](https://github.com/pytorch/pytorch/pull/59830))

## Dataloader

* Fixed `IterableFecher` to stop fetching data after `StopIterator` ([#59313](https://github.com/pytorch/pytorch/pull/59313))
* Fixed `ExceptionWrapper` to re-raise Exception with multiple args ([#58131](https://github.com/pytorch/pytorch/pull/58131))

## AMD

* Fix ROCm compilation by properly marking c++ functions as CPU only ([#62628](https://github.com/pytorch/pytorch/pull/62628))
* Fixed `torch.{i1,i1e}` ROCm failure: mark array as const so that it is available for host and device ([#59187](https://github.com/pytorch/pytorch/pull/59187))

## CUDA

* Fixed to not use deprecated data accessor in IndexKernel.cu ([#62268](https://github.com/pytorch/pytorch/pull/62268))
* Fixed sign comparison ([#62194](https://github.com/pytorch/pytorch/pull/62194), [#62483](https://github.com/pytorch/pytorch/pull/62483))
* Fixed `torch.manual_seed{_all}` memory leak ([#62534](https://github.com/pytorch/pytorch/pull/62534))
* Fixed CUDA_KERNEL_ASSERT ambiguous symbol in NDEBUG mode ([#62527](https://github.com/pytorch/pytorch/pull/62527))
* Changed to use long index type for `torch.index_add` deterministic implementation ([#59254](https://github.com/pytorch/pytorch/pull/59254))
* Fixed illegal memory access on NHWC BN kernel ([#59981](https://github.com/pytorch/pytorch/pull/59981))
* Fixed typo in Normalization.cu ([#62515](https://github.com/pytorch/pytorch/pull/62515))
* Added change to ignore and clear errors related to cuda not being ready yet ([#61554](https://github.com/pytorch/pytorch/pull/61554))
* Fixed segmentation fault due to access to destroyed global IPC variable([#56141](https://github.com/pytorch/pytorch/pull/56141))
* Fixed reduction launch config ([#64304](https://github.com/pytorch/pytorch/pull/64304))
* Fixed typo embedding_renorm_ cuda implementation ([#64542](https://github.com/pytorch/pytorch/pull/64542))
* Added missing kernel checks ([#60635](https://github.com/pytorch/pytorch/pull/60635))
* CUDA graphs: made sure graph mempool malloc counter pairs with frees for all allocations ([#61567](https://github.com/pytorch/pytorch/pull/61567))
* Fix bug where some kernels would not properly call cuda lazy initialization ([#61882](https://github.com/pytorch/pytorch/pull/61882))
* Added check for contiguous to dispatch to NHWC CUDA template ([#62839](https://github.com/pytorch/pytorch/pull/62839))
* Moved grid_sampler to autocast promote list ([#58618](https://github.com/pytorch/pytorch/pull/58618))
* Added check for memory overlap in sort for large input sizes ([#58327](https://github.com/pytorch/pytorch/pull/58327))

## C++ API

* Fixed `map` function for `vec256` to accept const pointer to function ([#59957](https://github.com/pytorch/pytorch/pull/59957))
* Added `supports_as_strided` method to `Device` and fixed indices of `to_sparse()` contiguous on all devices ([#59370](https://github.com/pytorch/pytorch/pull/59370))
* Removed redundant bitwise-and op in MT19937RNGEngine ([#63219](https://github.com/pytorch/pytorch/pull/63219))
* Fixed subprocess encoding for cpp extension on Windows ([#63756](https://github.com/pytorch/pytorch/pull/63756))
* Define the SYCL device version `__assert_fail` when the NDEBUG defined. ([#58906](https://github.com/pytorch/pytorch/pull/58906))

## TorchScript

* Fixed inconsistency between Python and JIT power operation ([#62842](https://github.com/pytorch/pytorch/pull/62842))
* Added change to convert `__constants__` attribute in model to a set to be consistent ([#60003](https://github.com/pytorch/pytorch/pull/60003)) 
* Added change to Ignore unsupported attribute checker pass for `torch.jit.trace` ([#60200](https://github.com/pytorch/pytorch/pull/60200)) 
* Fixed missing element types and shapes when `torch.autograd.Function` has multiple tensor outputs ([#57966](https://github.com/pytorch/pytorch/pull/57966))
* Fixed `Tensor.to` schema to reflect that the output may alias input ([#60001](https://github.com/pytorch/pytorch/pull/60001))  
* Added change to turn off layer norm in jit symbolic differentiation ([#63816](https://github.com/pytorch/pytorch/pull/63816)) 
* Fixed name conflict by using a more specific prefix for lowered module name. ([#61007](https://github.com/pytorch/pytorch/pull/61007)) 
* Added change to allow disabling cache in autocast (automatic mixed precision) ([#63552](https://github.com/pytorch/pytorch/pull/63552)) 
* Fixed concat optimization to handle cases when input list is mutated after cat using AliasDb ([#60774](https://github.com/pytorch/pytorch/pull/60774)) 
* Fixed symbolic derivative of hardswish ([#59405](https://github.com/pytorch/pytorch/pull/59405)) 

## torch.package

* Fixed a bug when using `importlib.resources.path` for python <3.8.8 ([#58718](https://github.com/pytorch/pytorch/pull/58718))
* Fixed bugs when using `os` and `os.path` ([#60276](https://github.com/pytorch/pytorch/pull/60276))
* Fixed storage serialization collision when saving a `ScriptModule` and then saving a `Tensor` owned by it. ([#61806](https://github.com/pytorch/pytorch/pull/61806))
* Fixed use-after-free during autograd shutdown ([#64620](https://github.com/pytorch/pytorch/pull/64620))
* Fixed non-determinism in naming scheme of serialized storages in export code paths and ABA ABA storage identity problem during serialization for `torch.package` ([#59735](https://github.com/pytorch/pytorch/pull/59735))
* Fixed GIL issue when acquiring multiple sessions. ([#58584](https://github.com/pytorch/pytorch/pull/58584))

## Mobile

* Fixed Nnapi backend dangling pointer bug ([#63092](https://github.com/pytorch/pytorch/pull/63092))
* Fixed missing constants archive in torchscript model after backport ([#58892](https://github.com/pytorch/pytorch/pull/58892))
* Fixed type hints in optimize_for_mobile to be consistent with the default([#59282](https://github.com/pytorch/pytorch/pull/59282))
* Fixed xnnpack hardswish memory issue ([#59577](https://github.com/pytorch/pytorch/pull/59577), [#61622](https://github.com/pytorch/pytorch/pull/61622))
* Fixed the issue that model_dump didn’t work with delegate models ([#61043](https://github.com/pytorch/pytorch/pull/61043))
* Fixed concat shaders didn’t work for certain iOS devices ([#61074](https://github.com/pytorch/pytorch/pull/61074))
* Fixed the Metal `torch.clamp` shader function for x86_64 ([#63062](https://github.com/pytorch/pytorch/pull/63062))
* Fixed callstack pointer serialization bug ([#63576](https://github.com/pytorch/pytorch/pull/63576))
* Fixed model loading error for Vulkan backend in Java API ([#63402](https://github.com/pytorch/pytorch/pull/63402))
* Fixed the issue that sub modules with same names are not serialized correctly in bytecode format ([#61933](https://github.com/pytorch/pytorch/pull/61933))

## Quantization

* Fixed crash when model outputs dicts or lists ([#58416](https://github.com/pytorch/pytorch/pull/58416))
* QAT: Fixed the runtime run `cannot resize variables that require grad` ([#57068](https://github.com/pytorch/pytorch/pull/57068))
* Fixed support for custom module ([#59041](https://github.com/pytorch/pytorch/pull/59041))
* Fixed the "tensors to be on the same device" error in HistogramObserver ([#59234](https://github.com/pytorch/pytorch/pull/59234))
* Fixed dimension for output of batchnorm 1d ([#59264](https://github.com/pytorch/pytorch/pull/59264))
* Fixed quantized mean operator in QNNPACK backend ([#59761](https://github.com/pytorch/pytorch/pull/59761))
* Fixed a bug in .to for qtensors so scale/zp move too ([#61576](https://github.com/pytorch/pytorch/pull/61576))
* Fixed quantized Conv1d module parameters ([#62356](https://github.com/pytorch/pytorch/pull/62356))
* Fixed quantization for tuple arguments ([#63376](https://github.com/pytorch/pytorch/pull/63376))
* Fixed fuse qconfig comparison ([#63384](https://github.com/pytorch/pytorch/pull/63384))
* Fixed the conversion of the quantizable RNN ([#63879](https://github.com/pytorch/pytorch/pull/63879))
* Fixed quantization for sub_scalar ([#64603](https://github.com/pytorch/pytorch/pull/64603))
* Fixed a bug for sub ([#65109](https://github.com/pytorch/pytorch/pull/65109))
* Add change to ensure qconfig works for QAT with multiple modules ([#63343](https://github.com/pytorch/pytorch/pull/63343))

## Distributed

`DistributedDataParallel`

* Fixed Pipe + DDP for unused parameters, static graph ([#60118](https://github.com/pytorch/pytorch/pull/60118))
* Fixed case where new tensors with no grad_fn are returned in DDP forward. ([#60882](https://github.com/pytorch/pytorch/pull/60882))
* Re-enabled the optimization of fusing copy and division when no comm hook is specified for both dense and sparse tensors ([#61379](https://github.com/pytorch/pytorch/pull/61379), [#61814](https://github.com/pytorch/pytorch/pull/61814))
* Fixed fp16 C++ DDP gradient communication hook ([#63375](https://github.com/pytorch/pytorch/pull/63375))
* Added change to ensure buffers are broadcasted properly when they are reassigned in module ([#64776](https://github.com/pytorch/pytorch/pull/64776))
* Fixed GradBucket.is_last() logic ([#63768](https://github.com/pytorch/pytorch/pull/63768))


`torch.distributed.Store`

* torch.distributed and RPC cannot both be initialized with the same host:port pair ([#58328](https://github.com/pytorch/pytorch/pull/58328), [#58329](https://github.com/pytorch/pytorch/pull/58329), [#58330](https://github.com/pytorch/pytorch/pull/58330), [#58331](https://github.com/pytorch/pytorch/pull/58331))

`torch.distributed.rpc`

* Added change to run dist_autograd backward RPCs on appropriate CUDA streams. ([#60606](https://github.com/pytorch/pytorch/pull/60606))
* Fixed race condition in TensorPipe agent ([#58753](https://github.com/pytorch/pytorch/pull/58753))
* Fixed issue when some gradients are None for distributed optimizers ([#62249](https://github.com/pytorch/pytorch/pull/62249))

`torch.distributed.elastic`

* Added change to ensure rendezvous timeout does not get overwritten ([#61471](https://github.com/pytorch/pytorch/pull/61471))
* Fixed the edge case when no node is alive ([#59663](https://github.com/pytorch/pytorch/pull/59663))
* Added change to cast timestamp type to int ([#59712](https://github.com/pytorch/pytorch/pull/59712))
* Added properly formatted traceback on error ([#65041](https://github.com/pytorch/pytorch/pull/65041))

`torch.distributed.autograd`

* Updated GraphTask::owner_ in a single thread for DistEngine. ([#58625](https://github.com/pytorch/pytorch/pull/58625))
* Introduced the deadlock fix ([#61588](https://github.com/pytorch/pytorch/pull/61588), [#61593](https://github.com/pytorch/pytorch/pull/61593))

`torch.distributed`

* Fixed the slowdown of _object_to_tensor since 1.9 (#65721) ([#65721](https://github.com/pytorch/pytorch/pull/65721))

## torch.fx

* Fixed retracing wrapped functions ([#58061](https://github.com/pytorch/pytorch/pull/58061))
* Added override for call_function so that wrapped functions stay wrapped ([#60057](https://github.com/pytorch/pytorch/pull/60057))
* Added fix to retain node.meta after normalizing args ([#60449](https://github.com/pytorch/pytorch/pull/60449))
* Added change to skip the output nodes but process possible nodes after it, when creating a single partition  ([#60370](https://github.com/pytorch/pytorch/pull/60370))
* Fixed fx patch module name ([#61062](https://github.com/pytorch/pytorch/pull/61062))
* Fixed graph `copy.deepcopy` to propagate output type ([#61747](https://github.com/pytorch/pytorch/pull/61747))
* Added change to allow starter nodes to depend on `get_attr` node ([#62234](https://github.com/pytorch/pytorch/pull/62234))
* Added change to prevent implicit submodule inlining when submodule is a GraphModule ([#62436](https://github.com/pytorch/pytorch/pull/62436))
* Added change to persist `tracer_cls` on `fx.Graph` when deep copying ([#63353](https://github.com/pytorch/pytorch/pull/63353))
* Fixed GraphModule deepcopy to use deepcopied graph ([#63090](https://github.com/pytorch/pytorch/pull/63090))
* Fixed constant folding for attrs in submodule hierarchies ([#64342](https://github.com/pytorch/pytorch/pull/64342))
* Fixed some const fold cases with deep model hierarchy ([#64945](https://github.com/pytorch/pytorch/pull/64945))
* Fixed tracing of bitwise and/or ([#65196](https://github.com/pytorch/pytorch/pull/65196))

## ONNX

* Added shape type inference fixes for control flow ([#60248](https://github.com/pytorch/pytorch/pull/60248))
* Fixed sum export with attribute `keepdims` ([#60245](https://github.com/pytorch/pytorch/pull/60245))
* Fixed shape inference for large model ([#60244](https://github.com/pytorch/pytorch/pull/60244))
* Fixed split export in op set 13 ([#57605](https://github.com/pytorch/pytorch/pull/57605))
* Fixed control-flow shape inference with contrib op ([#62762](https://github.com/pytorch/pytorch/pull/62762))
* Updated `instance_norm2d` export to handle `track_running_stats=True` ([#58690](https://github.com/pytorch/pytorch/pull/58690))
* Fixed the issue of converting empty list to sequence([#61558](https://github.com/pytorch/pytorch/pull/61558))
* Fixed sum could not be exported for empty tensor ([#59537](https://github.com/pytorch/pytorch/pull/59537))
* Fixed an issue that optimizations might adjust graph inputs unexpectedly ([#62763](https://github.com/pytorch/pytorch/pull/62763))

## Vulkan

* Fixed an issue where comparing equivalent descriptors would evaluate to `false` ([#60199](https://github.com/pytorch/pytorch/pull/60199))
* Fixed asserts in Vulkan JIT passes to actually throw an exception ([#61495](https://github.com/pytorch/pytorch/pull/61495))

## Performance_as_a_product

* Added fix to ensure number of thread utilities are initialized before getting the number of threads ([#60185](https://github.com/pytorch/pytorch/pull/60185))
* Added fix to ensure thread id is valid in nested parallel regions ([#60183](https://github.com/pytorch/pytorch/pull/60183))
* Fixed parallel tbb build ([#60532](https://github.com/pytorch/pytorch/pull/60532))
* Added change to make flags in the pytorch managed thread pool atomic. ([#58457](https://github.com/pytorch/pytorch/pull/58457))
* Set mkl thread locally ([#62891](https://github.com/pytorch/pytorch/pull/62891))

## Composability

* Added a fix to ensure that the C++ API’s that skip the dispatcher (such as `at::cpu::{op}` and `at::cuda::{op}` get external linkage, so they can be used outside of libtorch ([#58569](https://github.com/pytorch/pytorch/pull/58569))
* Fixed bug where shared memory tensor file names can collide ([#60978](https://github.com/pytorch/pytorch/pull/60978))

## Build_Frontend

* Fixed binary building without python ([#66031](https://github.com/pytorch/pytorch/pull/66031))
* Fixed Windows ninja builds when MAX_JOBS is specified ([#65444](https://github.com/pytorch/pytorch/pull/65444))
* Skipped Bfloat16 support when building for VSX ([#61630](https://github.com/pytorch/pytorch/pull/61630))
* Made change to use python3 alias in Makefile ([#58786](https://github.com/pytorch/pytorch/pull/58786))
* Made change to use `pybind11` from `third_party` folder by default ([#58951](https://github.com/pytorch/pytorch/pull/58951))
* Made change to ensure FindLAPACK finds the same BLAS library ([#49647](https://github.com/pytorch/pytorch/pull/49647))
* Improved Python package detection in `torch.utils.collect_env` ([#63321](https://github.com/pytorch/pytorch/pull/63321))
* Skipped SVE acceleration on M1 machine ([#58785](https://github.com/pytorch/pytorch/pull/58785))
* Made `SciPy` dependency optional in PyTorch unary operators tests ([#59304](https://github.com/pytorch/pytorch/pull/59304))
* Fixed error-handling when Python executable can not be found ([#61230](https://github.com/pytorch/pytorch/pull/61230))
* Fixed `setup.py` re-run incremental build logic on Windows ([#59689](https://github.com/pytorch/pytorch/pull/59689))
* Reduced binary size for CUDA-split build by establishing correct linking order ([#58287](https://github.com/pytorch/pytorch/pull/58287))
* Fixed  `torch.utils.cpp_extension` behavior when older setuptools are used ([#61484](https://github.com/pytorch/pytorch/pull/61484))

## Infra (Releng)

* Fixed windows ci squid env ([#62353](https://github.com/pytorch/pytorch/pull/62353))
* Introduced CI dependency pinning: ([#64922](https://github.com/pytorch/pytorch/pull/64922), [#65017](https://github.com/pytorch/pytorch/pull/65017))
* Fixed breakpad build and add to more images ([#59236](https://github.com/pytorch/pytorch/pull/59236))
* Updated certificate trust chain CI to depend on the linked commits ([#65934](https://github.com/pytorch/pytorch/pull/65934), [#66004](https://github.com/pytorch/pytorch/pull/66004))

## LinAlg_Frontend

* Fixed an issue where the “info” tensor returned by `torch.linalg.inv_ex` could sometimes be on the wrong device ([#59223](https://github.com/pytorch/pytorch/pull/59223))
* Fixed an issue where `torch.linalg.norm` could return tensors with the wrong shape in some edge cases ([#60273](https://github.com/pytorch/pytorch/pull/60273))
* Fixed an issue where `torch.linalg.svd` could return tensors with the wrong shape in some edge cases ([#62022](https://github.com/pytorch/pytorch/pull/62022))
* Fixed an issue where `torch.matmul` would throw an error when attempting to multiply certain empty tensors ([#63359](https://github.com/pytorch/pytorch/pull/63359))

## Sparse_Frontend

* Fixed dtype inference in sparse_csr_tensor_ctor ([#58631](https://github.com/pytorch/pytorch/pull/58631))
* Fixed addmm failure for CSR Tensors when MKL is not available ([#58768](https://github.com/pytorch/pytorch/pull/58768))
* Fixed overflow of numel for sparse COO tensors after calling coalesce ([#57492](https://github.com/pytorch/pytorch/pull/57492))
* Fixed multiplication of 0-dim Tensor and COO sparse Tensor and improved Error message for multiplication of dense and sparse COO tensor ([#61723](https://github.com/pytorch/pytorch/pull/61723))
* Fixed internal assert error for CSR tensors crow_/col_indices methods in Debug build ([#63176](https://github.com/pytorch/pytorch/pull/63176))
* Fixed support of torch.conj for zero-dimensional sparse COO Tensors ([#59553](https://github.com/pytorch/pytorch/pull/59553))

## Misc

* Added change to increase warmup for better steady state measurements. ([#58801](https://github.com/pytorch/pytorch/pull/58801))
* Fixed bad use of channels last kernel in sync batch norm backward ([#64100](https://github.com/pytorch/pytorch/pull/64100))

# Performance

## Python API

* `torch.special.{'i0', 'i0e', 'i1', 'i1e'}:` converted floating-point constants to input type in Bessel functions ([#59416](https://github.com/pytorch/pytorch/pull/59416))
* Added change to speed up `torch.unique_consecutive()` ([#64835](https://github.com/pytorch/pytorch/pull/64835))
* Made sure all graphs tests call `torch.cuda.empty_cache()` before capture to fix flaky tests ([#59233](https://github.com/pytorch/pytorch/pull/59233))
* `torch.flip` : improved performance via TensorIterator ([#59509](https://github.com/pytorch/pytorch/pull/59509))
* Added change to parallelize `torch.gelu` via tensoriterator ([#58950](https://github.com/pytorch/pytorch/pull/58950))
* `torch.sum`: added change to accumulate 16-bit float sums in 32-bit accumulators for improved precision and performance ([#60387](https://github.com/pytorch/pytorch/pull/60387))
* Added fast path for conjugated tensors for  `torch.`{`dot, vdot, mm, addmm, bmm, baddbmm}` ([#62915](https://github.com/pytorch/pytorch/pull/62915), [#59380](https://github.com/pytorch/pytorch/pull/59380))

## Autograd

* Faster `torch.cum{sum,prod}` backward formulas ([#60642](https://github.com/pytorch/pytorch/pull/60642))
* Reduced overhead from `reshape` call if the tensor already has the right shape ([#61466](https://github.com/pytorch/pytorch/pull/61466))
* Added change to speed up saving variables for backward ([#59837](https://github.com/pytorch/pytorch/pull/59837), [#61927](https://github.com/pytorch/pytorch/pull/61927))
* Reduced number of TLS access when deciding if an op needs to be tracked by autograd or not ([#60740](https://github.com/pytorch/pytorch/pull/60740))
* Improved code that detect when it is valid to re-use existing Tensors during the backward pass ([#59817](https://github.com/pytorch/pytorch/pull/59817))

## torch.nn

* `nn.utils.clip_grad_norm_`: Removed device syncs ([#61042](https://github.com/pytorch/pytorch/pull/61042))
* `nn.BatchNorm2d`: Optimized performance for `channels_last` on CPU ([#59286](https://github.com/pytorch/pytorch/pull/59286))
* `nn.Softmax`: Vectorized softmax calculation for the non-last-dimension case ([#59195](https://github.com/pytorch/pytorch/pull/59195), [#60371](https://github.com/pytorch/pytorch/pull/60371))
* `nn.Transformer`: Faster `generate_square_subsequent_mask` ([#60631](https://github.com/pytorch/pytorch/pull/60631))

## CUDA

* Updated launch bounds for trilinear 3d ([#59999](https://github.com/pytorch/pytorch/pull/59999))
* Migrated Embedding thrust sort to cub sort ([#62495](https://github.com/pytorch/pytorch/pull/62495))
* Make `unique` call in embedding use cub instead of thrust ([#63042](https://github.com/pytorch/pytorch/pull/63042))
* Migrated masked_scatter to use cub instead of thrust ([#56750](https://github.com/pytorch/pytorch/pull/56750))
* Reverted D28547564: [pytorch][PR] masked_scatter thrust→cub ([9e261de630](https://github.com/pytorch/pytorch/commit/9e261de630))
* Make sort in EmbeddingBag use cub instead of thrust ([#64498](https://github.com/pytorch/pytorch/pull/64498))
* Migrated Embedding thrust sort to cub sort ([#63806](https://github.com/pytorch/pytorch/pull/63806))
* Removed cat, equal, and stack from autocast promote list ([#59497](https://github.com/pytorch/pytorch/pull/59497))
* Add cublas and cusolver paths for LU solve ([#59148](https://github.com/pytorch/pytorch/pull/59148))
* Fixed launch bounds for gathertopk kernel ([#60314](https://github.com/pytorch/pytorch/pull/60314))
* Changed launch bounds, unrolled for loop for grid sampler 2d fwd and bwd ([#60405](https://github.com/pytorch/pytorch/pull/60405))
* Changed launch bound to fix col2im kernel ([#60315](https://github.com/pytorch/pytorch/pull/60315))
* Fixed launch bounds for grid sampler 3d ([#60385](https://github.com/pytorch/pytorch/pull/60385))
* CUDA graphs: added change to not sync between replays for CUDA driver version 11.4+ ([#61063](https://github.com/pytorch/pytorch/pull/61063))
* Changed launch bounds for upsample_linear1d fwd, bwd from 1024 to 512 ([#61307](https://github.com/pytorch/pytorch/pull/61307))
* Added change to reduce max_num_threads for complex double ops in reduce_kernel ([#61438](https://github.com/pytorch/pytorch/pull/61438))
* Added change to use `fastAtomicAdd` in EmbeddingBag (mode "max") backward ([#63298](https://github.com/pytorch/pytorch/pull/63298))
* Added change to use multi-dimensional cuFFT transforms to improve FFT performance ([#61203](https://github.com/pytorch/pytorch/pull/61203))
* `F.avg_pool3d` CUDA backward: use fast atomic adds ([#63387](https://github.com/pytorch/pytorch/pull/63387))
* Add cuSOLVER path for LU factorization in CUDA. ([#56887](https://github.com/pytorch/pytorch/pull/56887))
* Reverted launch bounds change in topK that induced a regression in perf ([#63431](https://github.com/pytorch/pytorch/pull/63431))
* Added change to bring back old algorithm for sorting on small number of segments ([#64127](https://github.com/pytorch/pytorch/pull/64127))

## Mobile

* Added change to use channel-last to transform the weights for Metal ([#59113](https://github.com/pytorch/pytorch/pull/59113))
* Implemented RoIAlign in Metal shaders using Sampler ([#56075](https://github.com/pytorch/pytorch/pull/56075))
* Added cache operator lambda during model loading ([#61996](https://github.com/pytorch/pytorch/pull/61996))
* Added Operator Call De-dup at TorchScript Serialization Level ([#64269](https://github.com/pytorch/pytorch/pull/64269))
* Added change to speed up model loading by 1directly calling the C file API from FileAdapter ([#61997](https://github.com/pytorch/pytorch/pull/61997))
* Moved from input ivalues in ByteCodeDeserializer ([#64029](https://github.com/pytorch/pytorch/pull/64029))
* Fixed MobileDebugInfo vector copy ([#64030](https://github.com/pytorch/pytorch/pull/64030))
* Added change to gate tls_local_dispatch_key_set off on iOS too ([#64753](https://github.com/pytorch/pytorch/pull/64753))
* Added change to not store multiple kernels per key on mobile ([#64447](https://github.com/pytorch/pytorch/pull/64447))
* Added OpCode cache in ByteCodeDeserializer ([#64110](https://github.com/pytorch/pytorch/pull/64110))
* Reduced mobile model size by reusing constant and bump bytecode to v5 ([#59722](https://github.com/pytorch/pytorch/pull/59722))

## Distributed

* `torch.distributed:` replaced all_gather with more efficient collective api _all_gather_base ([#57769](https://github.com/pytorch/pytorch/pull/57769))
* `torch.distributed.optim.ZeroRedundancyOptimizer: `Sorted params by size (decreasing) ([#59586](https://github.com/pytorch/pytorch/pull/59586))

## Vulkan

* Improved the performance of pointwise convolutions by having each shader invocation calculate a 4x4 output tile  ([#60760](https://github.com/pytorch/pytorch/pull/60760))
* Implemented a simple scheme to set the local work group size adaptively ([#61170](https://github.com/pytorch/pytorch/pull/61170))

## Performance_as_a_product

* TensorIterator: added change to reduce serial_for_each static overhead ([#58909](https://github.com/pytorch/pytorch/pull/58909))
* Added change to avoid using `std::regex` for device string parsing ([#63204](https://github.com/pytorch/pytorch/pull/63204))

## Composability

* Introduced some perf improvements for reduction ops ([#58655](https://github.com/pytorch/pytorch/pull/58655))
* Added optimization to some internal representations of sizes ([#59333](https://github.com/pytorch/pytorch/pull/59333))
* Reduced the number of tensor refcount bumps in many existing kernels ([#58303](https://github.com/pytorch/pytorch/pull/58303), [#59827](https://github.com/pytorch/pytorch/pull/59827), [#58273](https://github.com/pytorch/pytorch/pull/58273), [#58272](https://github.com/pytorch/pytorch/pull/58272), [#58276](https://github.com/pytorch/pytorch/pull/58276), [#58277](https://github.com/pytorch/pytorch/pull/58277), [#58279](https://github.com/pytorch/pytorch/pull/58279), [#60546](https://github.com/pytorch/pytorch/pull/60546), [#58280](https://github.com/pytorch/pytorch/pull/58280))
* Added micro-optimizations to improve the time it takes to load pytorch ([#64784](https://github.com/pytorch/pytorch/pull/64784), [#64820](https://github.com/pytorch/pytorch/pull/64820), [#64821](https://github.com/pytorch/pytorch/pull/64821), [#64822](https://github.com/pytorch/pytorch/pull/64822), [#64838](https://github.com/pytorch/pytorch/pull/64838), [#64678](https://github.com/pytorch/pytorch/pull/64678), [#64682](https://github.com/pytorch/pytorch/pull/64682), [#64670](https://github.com/pytorch/pytorch/pull/64670))

## Build_Frontend

* Compiled BatchLinearAlgebra CUDA integration routines with host compiler ([#64146](https://github.com/pytorch/pytorch/pull/64146))
* Sped-up compilation by splitting autogenerated files into smaller ones ([#62186](https://github.com/pytorch/pytorch/pull/62186))
* Allowed [ninja-build](https://ninja-build.org/) to dynamically pick best parallel build option ([#64733](https://github.com/pytorch/pytorch/pull/64733), [#65162](https://github.com/pytorch/pytorch/pull/65162))

## Infra (Releng)

* .github: upload /download large artifacts to s3 ([#58506](https://github.com/pytorch/pytorch/pull/58506))
* Made change to only run mem leak check on master ([#60023](https://github.com/pytorch/pytorch/pull/60023))
* Enabled parallel clang-tidy on ec2 runner ([#60870](https://github.com/pytorch/pytorch/pull/60870))
* Made change to skip magma library installation for Windows CPU builds ([#59619](https://github.com/pytorch/pytorch/pull/59619))

## Sparse_Frontend

* Sped up conversion of COO to CSR Tensor `to_sparse_csr` by writing custom CPU/GPU kernels ([#61340](https://github.com/pytorch/pytorch/pull/61340), [#61838](https://github.com/pytorch/pytorch/pull/61838))
* Slightly sped up calculation of number of dense entries for sparse softmax via `c10::multiply_integers`  for COO Tensors ([#60872](https://github.com/pytorch/pytorch/pull/60872))
* Slightly sped up sparse softmax for COO Tensors by improve usage of `std::vector` ([#60873](https://github.com/pytorch/pytorch/pull/60873))
* Sped up index_select for sparse COO Tensor ([#63008](https://github.com/pytorch/pytorch/pull/63008))

## Misc

* Greatly reduced the post-processing time of the profiler ([#60432](https://github.com/pytorch/pytorch/pull/60432))
* Saved some little memory in `default_collate` ([#61424](https://github.com/pytorch/pytorch/pull/61424))
* Added new ops to the operator microbenchmark: `gelu`, `bmm`, `mm`, `einsum`, `log1p` ([#59334](https://github.com/pytorch/pytorch/pull/59334), [#59595](https://github.com/pytorch/pytorch/pull/59595), [#63654](https://github.com/pytorch/pytorch/pull/63654), [#64647](https://github.com/pytorch/pytorch/pull/64647), [#64032](https://github.com/pytorch/pytorch/pull/64032), [#64205](https://github.com/pytorch/pytorch/pull/64205))
* Added AVX512 support in ATen & remove AVX support ([#61903](https://github.com/pytorch/pytorch/pull/61903))


You can also find the dev specific and documentation related changes in the forum post [here](https://dev-discuss.pytorch.org/t/pytorch-1-10-dev-release-notes/379)
# ===== RELEASE pytorch/pytorch v1.12.0 =====

# PyTorch 1.12 Release Notes

* Highlights
* Backwards Incompatible Change
* New Features
* Improvements
* Performance
* Documentation

# Highlights

We are excited to announce the release of PyTorch 1.12! This release is composed of over 3124 commits, 433 contributors. Along with 1.12, we are releasing beta versions of AWS S3 Integration, PyTorch Vision Models on Channels Last on CPU, Empowering PyTorch on Intel® Xeon® Scalable processors with Bfloat16 and FSDP API. We want to sincerely thank our dedicated community for your contributions. 

Summary:

* Functional Module API to functionally apply module computation with a given set of parameters
* Complex32 and Complex Convolutions in PyTorch 
* DataPipes from TorchData fully backward compatible with DataLoader 
* Functorch with improved coverage for APIs
* nvFuser a deep learning compiler for PyTorch
* Changes to float32 matrix multiplication precision on Ampere and later CUDA hardware
* TorchArrow, a new beta library for machine learning preprocessing over batch data

# Backwards Incompatible changes

## Python API

**Updated type promotion for `torch.clamp`** ([#77035](https://github.com/pytorch/pytorch/pull/77035))

In 1.11, the ‘min’ and ‘max’ arguments in `torch.clamp` did not participate in type promotion, which made it inconsistent with `minimum` and `maximum` operations. In 1.12, the ‘min’ and ‘max’ arguments participate in type promotion.

1.11

```python
>>> import torch
>>> a = torch.tensor([1., 2., 3., 4.], dtype=torch.float32)
>>> b = torch.tensor([2., 2., 2., 2.], dtype=torch.float64)
>>> c = torch.tensor([3., 3., 3., 3.], dtype=torch.float64)
>>> torch.clamp(a, b, c).dtype
torch.float32
```

1.12

```python
>>> import torch
>>> a = torch.tensor([1., 2., 3., 4.], dtype=torch.float32)
>>> b = torch.tensor([2., 2., 2., 2.], dtype=torch.float64)
>>> c = torch.tensor([3., 3., 3., 3.], dtype=torch.float64)
>>> torch.clamp(a, b, c).dtype
torch.float64
```

## Complex Numbers

### Fix complex type promotion ([#77524](https://github.com/pytorch/pytorch/pull/77524))

Updates the type promotion rule such that given a complex scalar and real tensor, the value type of real tensor is preserved 

1.11

```python
>>> a = torch.randn((2, 2), dtype=torch.float)
>>> b = torch.tensor(1, dtype=torch.cdouble)
>>> (a + b).dtype
torch.complex128
```

1.12

```python
>>> a = torch.randn((2, 2), dtype=torch.float)
>>> b = torch.tensor(1, dtype=torch.cdouble)
>>> (a + b).dtype
torch.complex64
```

## LinAlg

### Disable TF32 for matmul by default and add high-level control of fp32 matmul precision ([#76509](https://github.com/pytorch/pytorch/pull/76509))

PyTorch 1.12 makes the default math mode for fp32 matrix multiplications more precise and consistent across hardware. This may affect users on Ampere or later CUDA devices and TPUs. See the PyTorch [blog](https://dev-discuss.pytorch.org/t/pytorch-and-tensorfloat32/504) for more details. 

## Sparse

### Use ScatterGatherKernel for scatter_reduce (CPU-only) ([#74226](https://github.com/pytorch/pytorch/pull/74226), [#74608](https://github.com/pytorch/pytorch/pull/74608))

In 1.11.0, unlike `scatter` which takes a `reduce` kwarg or `scatter_add`, `scatter_reduce` was not an in-place function. That is, it did not allow the user to pass an output tensor which contains data that is reduced together with the scattered data. Instead, the scatter reduction took place on an output tensor initialized under the hood. Indices of the output that were not scattered to were filled with reduction inits (or 0 for options ‘amin’ and ‘amax’).

In 1.12.0, `scatter_reduce` (which is in beta) is in-place to align with the API of the related existing functions `scatter`/`scatter_add`. For this reason, the argument `input` in 1.11.0 has been renamed `src` in 1.12.0 and the new `self` argument now takes a destination tensor to be scattered onto. Since the destination tensor is no longer initialized under the hood, the `output_size` kwarg in 1.11.0 that allowed users to specify the size of the output at dimension `dim` has been removed. Further, in 1.12.0 we introduce an `include_self` kwarg which determines whether values in the `self` (destination) tensor are included in the reduction. Setting `include_self=True` could, for example, allow users to provide special reduction inits for the scatter_reduction operation. Otherwise, if `include_self=False,` indices scattered to are treated as if they were filled with reduction inits.

In the snippet below, we illustrate how the behavior of `scatter_reduce` in 1.11.0 can be achieved with the function released in 1.12.0.

Example:

```python
>>> src = torch.arange(6, dtype=torch.float).reshape(3, 2)
>>> index = torch.tensor([[0, 2], [1, 1], [0, 0]])
>>> dim = 1
>>> output_size = 4
>>> reduce = "prod"
```

1.11

```python
>>> torch.scatter_reduce(src, dim, index, reduce, output_size=output_size)
`tensor([[ 0., 1., 1., 1.],
        [ 1., 6., 1., 1.],
        [20., 1., 1., 1.]])`
```

1.12

```python
>>> output_shape = list(src.shape)
>>> output_shape[dim] = output_size
# reduction init for prod is 1
# filling the output with 1 is only necessary if the user wants to preserve the behavior in 1.11
# where indices not scattered to are filled with reduction inits
>>> output = src.new_empty(output_shape).fill_(1)
>>> output.scatter_reduce_(dim, index, src, reduce)
`tensor([[ 0., 1., 1., 1.],
        [ 1., 6., 1., 1.],
        [20., 1., 1., 1.]])`
```

## torch.nn

### `nn.GroupNorm`: Report an error if `num_channels` is not divisible by `num_groups` ([#74293](https://github.com/pytorch/pytorch/pull/74293))

Previously, `nn.GroupNorm` would error out during the forward pass if `num_channels` is not divisible by `num_groups`. Now, the error is thrown for this case during module construction instead.

1.11

```python
m = torch.nn.GroupNorm(3, 7)
m(...)  # errors during forward pass
```

1.12

```python
m = torch.nn.GroupNorm(3, 7)  # errors during construction
```

### `nn.Dropout2d`: Return to 1.10 behavior: perform 1D channel-wise dropout for 3D inputs

In PyTorch 1.10 and older, passing a 3D input to `nn.Dropout2D` resulted in 1D channel-wise dropout behavior; i.e. such inputs were interpreted as having shape `(N, C, L)` with N = batch size and C = # channels and channel-wise dropout was performed along the second dimension.

1.10

```python
x = torch.randn(2, 3, 4)
m = nn.Dropout2d(p=0.5)
out = m(x)  # input is assumed to be shape (N, C, L); dropout along the second dim.
```

With the introduction of no-batch-dim input support in 1.11, 3D inputs were reinterpreted as having shape `(C, H, W)`; i.e. an input without a batch dimension, and dropout behavior was changed to drop along the first dimension. This was a silent breaking change.

1.11

```python
x = torch.randn(2, 3, 4)
m = nn.Dropout2d(p=0.5)
out = m(x)  # input is assumed to be shape (C, H, W); dropout along the first dim.
```

The breaking change in 1.11 resulted in a lack of support for 1D channel-wise dropout behavior, so `Dropout2d`  in PyTorch 1.12 returns to 1.10 behavior with a warning to give some time to adapt before the no-batch-dim interpretation goes back into effect.

1.12

```python
x = torch.randn(2, 3, 4)
m = nn.Dropout2d(p=0.5)
out = m(x)  # input is assumed to be shape (N, C, L); dropout along the second dim.
            # throws a warning suggesting nn.Dropout1d for 1D channel-wise dropout.
```

If you want 1D channel-wise dropout behavior, please switch to use of the newly-added `nn.Dropout1d` module instead of `nn.Dropout2d`. If you want no-batch-dim input behavior, please note that while this is not supported in 1.12, a future release will reinstate the interpretation of 3D inputs to `nn.Dropout2d` as those without a batch dimension.

### **`F.cosine_similarity`: Improve numerical stability ([#31378](https://github.com/pytorch/pytorch/pull/31378))**

Previously, we first compute the inner product, then normalize. After this change, we first normalize, then compute inner product. This should be more numerically stable because it avoids losing precision in inner product for inputs with large norms. Because of this change, outputs may be different in some cases.

## Composability

**Functions in torch.ops.aten.{foo} no longer accept `self` as a kwarg**

`torch.ops.aten.{foo}` objects are now instances of `OpOverloadPacket` (instead of a function) that have their `__call__` method in Python, which means that you cannot pass `self` as a kwarg. You can pass it normally as a positional argument instead.

1.11

```python
>>> torch.ops.aten.sin(self=torch.ones(2))
    tensor([0.8415, 0.8415])
```

1.12

```python
# this now fails
>>> torch.ops.aten.sin(self=torch.ones(2))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __call__() got multiple values for argument 'self'
# this works
>>> torch.ops.aten.sin(torch.ones(2))
tensor([0.8415, 0.8415])
```

**__torch_dispatch__ now traces individual op overloads instead of op overload packets (**[**#72673**](https://github.com/pytorch/pytorch/pull/72673)**)**

`torch.ops.aten.add` actually corresponds to a bundle of functions from C++, corresponding to all over the overloads of add operator (specifically, `add.Tensor`, `add.Scalar` and `add.out`). Now, `__torch_dispatch__` will directly take in an overload corresponding to a single aten function.

1.11

```python
class MyTensor(torch.Tensor):
    ....
    def __torch_dispatch__(cls, func, types, args=(), kwargs=None):
        # Before, func refers to a "packet" of all overloads
        # for a given operator, e.g. "add"
        assert func == torch.ops.aten.add
```

1.12

```python
class MyTensor(torch.Tensor):
    ....
    def __torch_dispatch__(cls, func, types, args=(), kwargs=None):
        # After, func refers to an individual operator overload,
        # e.g. "add.Tensor"
        assert func == torch.ops.aten.add.Tensor
        # you can recover the old behavior with func.overloadpacket
        assert func.overloadpacket == torch.ops.aten.add
```

## Profiler

### Disable forward-backward correlation ([#72904](https://github.com/pytorch/pytorch/pull/72904))

The forward-backward correlation is no longer captured as to workaround a profile crash. This feature may be reenabled in a future release after the underlying issue is fixed.

```python
with torch.profiler.profile() as p:
    loss = model(inputs)
    loss.backward()  # Invoke autograd

# The exported chrome trace will not have forward-backward flow events. (arrows)
p.export_chrome_trace(...)
```

## Mobile

### Remove support for bytecode version 3 ([#57775](https://github.com/pytorch/pytorch/pull/57775))

The minimum supported bytecode version is being bumped from 3 to 4. We no longer support version 3 bytecode models because the bytecode version was bumped from 3 to 4 more than half a year ago, and there was code in operator loading that performed differently on one operator on the global bytecode version 3. 

If the model is generated before Oct 5, 2020, please use the following lines to update the model to the latest version:

1.12

```python
import torch
from torch.jit.mobile import _get_model_bytecode_version

old_model_path = "old_model.ptl"
new_model_path = "new_model.ptl"

# Load full jit model
jit_model = torch.jit.load(old_model_path)
# Save model for mobile 
jit_model._save_for_lite_interpreter(new_model_path)
# Verify the model can be loaded
mobile_m = _load_for_lite_interpreter(new_model_path)

# Get bytecode version from the new model
bytecode_version = _get_model_bytecode_version(new_model_path)
print(f"bytecode version is {bytecode_version}")

```

### Remove redundant FSDP prefix and change default auto wrap policy name to avoid confusion ([#76858](https://github.com/pytorch/pytorch/pull/76858), [#73791](https://github.com/pytorch/pytorch/pull/73791))

`FullyShardedDataParallel`'s optional param name ‘fsdp_auto_wrap_policy’ (1.11) changed to ‘auto_wrap_policy’ (1.12). ‘default_auto_wrap_policy’ (1.11) is changed to ‘size_based_auto_wrap_policy’ (1.12). 

In 1.11, when wrapping a model with FSDP instead of:

```python
model = MyModel()
wrapped_model = FullyShardedDataParallel(
    model,
    **fsdp_auto_wrap_policy**=functools.partial(
        default_auto_wrap_policy,
        min_num_params=0,  # wrap all modules
    )
   ...
```

1.12

```python
model = MyModel()
wrapped_model = FullyShardedDataParallel(
    model,
   **auto_wrap_policy**=functools.partial(
        size_based_auto_wrap_policy,
        min_num_params=0,  # wrap all modules
    )
   ...
```

## Quantization

### TorchScript models exported prior to PyTorch 1.6 using quantized Linear, GRU and LSTM operators will no longer work ([#72680](https://github.com/pytorch/pytorch/pull/72680), [#72522](https://github.com/pytorch/pytorch/pull/72522)) 

TorchScript models created with PyTorch 1.5 or earlier and using the operators `quantized::linear_prepack_legacy`, `linear_prepack_fp16_legacy`, `quantized::linear_unpack.legacy`, or `quantized::linear_unpack_fp16.legacy` will no longer work and need to be re-exported. Please use PyTorch [Quantization](http://%20https//pytorch.org/docs/stable/quantization.html) to quantize the Linear module instead.

## ONNX

## Infra (Releng)

* Bump minimum CMake version to 3.13 ([#76312](https://github.com/pytorch/pytorch/pull/76312))

# Deprecations

## Python API

**Deprecated torch.testing.make_non_contiguous** ([#72705](https://github.com/pytorch/pytorch/pull/72705))

`torch.testing.make_non_contiguous` is being deprecated and will be removed in a future release. Depending on the use case there are different replacement options: If you are using `make_non_contiguous` in the PyTorch test suite, you can use ``torch.testing._internal.common_utils.noncontiguous_like``

1.11

```python
a = torch.randn(1, 2, 3)
torch.testing.make_non_contiguous(a)
```

1.12

```python
a = torch.randn(1, 2, 3)
torch.testing._internal.common_utils.noncontiguous_like(a)
```

If you are using `make_non_contiguous` in combination with a creation function to create a noncontiguous tensor with random values, you can use `make_tensor`.

1.11

```python
a = torch.randn(1, 2, 3)
torch.testing.make_non_contiguous(a)
```

1.12

```python
torch.testing.make_tensor(..., noncontiguous=True)
```

If you are using `make_non_contiguous` with a specific tensor, you can use `torch.repeat_interleave`

1.11

```python
a = torch.tensor([[1., 2.], [1., 2.]])
torch.testing.make_non_contiguous(a)
```

1.12

```python
a = torch.tensor([[1., 2.], [1., 2.]])
torch.repeat_interleave(input, 2, dim=-1)[..., ::2]
```

## Build

## LinAlg

### Deprecate torch.lu ([#73804](https://github.com/pytorch/pytorch/pull/73804))

`torch.lu()` is deprecated in favor of `torch.linalg.lu_factor()` and `torch.linalg.lu_factor_ex()`. `torch.lu()` will be removed in a future PyTorch release. If you were previously using `get_infos=False` (this is the default), you should use `torch.linalg.lu_factor` instead:

1.11

```python
LU, pivots = torch.lu(A, compute_pivots) 
```

1.12

```python
LU, pivots = torch.linalg.lu_factor(A, compute_pivots) 
```

If you were previously using `get_infos=True` you should use `torch.linalg.lu_factor_ex`:

1.11

```python
LU, pivots, info = torch.lu(A, compute_pivots, get_infos=True)
```

1.12

```python
LU, pivots, info = torch.linalg.lu_factor_ex(A, compute_pivots) 
```

### Deprecate torch.lu_solve ([#73806](https://github.com/pytorch/pytorch/pull/73806))

`torch.lu_solve()` is deprecated in favor of `torch.linalg.lu_solve()`. `torch.lu_solve()` will be removed in a future PyTorch release.

1.11

```python
X = torch.lu_solve(B, LU, pivots)
```

1.12

```python
X = torch.linalg.lu_solve(LU, pivots, B) 
```

### Remove deprecated torch.solve ([#70986](https://github.com/pytorch/pytorch/pull/70986))

`torch.solve` which was deprecated in a previous release is now being removed. You should use  `torch.linalg.solve`. instead. Note that `torch.linalg.solve` has its arguments reversed and does not return the LU factorization. To get the LU factorization see `torch.lu`, which can be used with `torch.lu_solve` or `torch.lu_unpack`.

1.11

```python
X = torch.solve(B, A).solution
```

1.12

```python
X = torch.linalg.solve(A, B)
```

## torch.nn

### `nn.Module`: Deprecate positional args for `state_dict()` ([#72780](https://github.com/pytorch/pytorch/pull/72780))

`state_dict` can currently be called in two ways: `destination`, `prefix`, and `keep_vars` can be passed as positional arguments, or as kwargs. The ability to do the former is being deprecated and will be removed in a future release. You should pass the arguments in as kwargs only. 

## Composability

**Deprecated `__torch_function__` as instance method for more functions** ([#74829](https://github.com/pytorch/pytorch/pull/74829))

`__torch_function__` should be defined as a class method. Defining `__torch_function__` as a plain method has already been previously deprecated for the functions handling `__torch_function__` in Python. This change makes it so that that is also the case for functions that handle `__torch_function__` in c++.

1.11

```python
class Bad():
    def __torch_function__(self, *args, **kwargs):
        pass
t = Bad()
torch.abs(t)
```

1.12

```python
class Good():
    @classmethod
    def __torch_function__(cls, *args, **kwargs):
        pass
t = Good()
torch.abs(t)
```

## Quantization

### Deprecate `torch.jit.quantized` ([#72690](https://github.com/pytorch/pytorch/pull/72690))

Instead of using functions defined in `torch.jit.quantized,` please use [PyTorch Quantization](https://pytorch.org/docs/stable/quantization.html) to dynamically quantize Linear/RNNCell/LSTMCell/GRUCell/LSTM modules. It’s both supported in [Eager Mode Quantization](http://%20https//pytorch.org/docs/stable/quantization.html#dynamic-quantization) and [FX Graph Mode Quantization](https://pytorch.org/tutorials/prototype/fx_graph_mode_ptq_dynamic.html)

1.11

```python
>> torch.jit.quantized.QuantizedLSTMCell(...)
```

1.12

```python
>> torch.jit.quantized.QuantizedLSTMCell(...)
   "torch.jit.QuantizedLSTMCell is deprecated and will be removed in an upcoming
    PyTorch release. Please use the torch.nn.quantized.dynamic.LSTMCell instead."
```

## Infra (Releng)

* Removed CUDA 11.1 binary builds ([#73376](https://github.com/pytorch/pytorch/pull/73376))
* Removed CUDA 11.5 binary builds ([#76257](https://github.com/pytorch/pytorch/pull/76257))

# New features

## Python API

* Added new device `mps` that can be used to leverage GPU acceleration on macOS platform with Apple Native Silicon (M1) or discrete AMD GPUs. ([blogpost with details](https://pytorch.org/blog/introducing-accelerated-pytorch-training-on-mac/))
* Added `torch.special.log_ndtr` ([#74795](https://github.com/pytorch/pytorch/pull/74795))
* Added `torch.distributions.transforms.{SoftplusTransform,CumulativeDistributionTransform}` ([#52300](https://github.com/pytorch/pytorch/pull/52300), [#72495](https://github.com/pytorch/pytorch/pull/72495))
* Promoted `torch.testing` to stable ([#73348](https://github.com/pytorch/pytorch/pull/73348))
* Added `maximize` flag for `optim.Adadelta`([#75330](https://github.com/pytorch/pytorch/pull/75330))

## Build

* Distributed torchgen as part of PyTorch package ([#76306](https://github.com/pytorch/pytorch/pull/76306))
* Added BUILD_LAZY_CUDA_LINALG option ([#73447](https://github.com/pytorch/pytorch/pull/73447))
* Introduced an environment variable to change c10 log level ([#71746](https://github.com/pytorch/pytorch/pull/71746))

## Complex Numbers

* Added a new data-type `torch.complex32` to help computing with complex datatype with lower memory usage at the cost of lower precision. Note that this is an experimental feature ([#78245](https://github.com/pytorch/pytorch/pull/78245)) and the major focus in this release was to support operators under `torch.fft` on CUDA.  Besides those operators we have added support and testing for following limited set of ops **(NOTE: few operators are only supported on CUDA)**: `Tensor.copy_, torch.complex, torch.testing.make_tensor, cat, Tensor.fill_, Tensor.item, torch.atleast_1d, torch.atleast_2d, torch.atleast_3d, torch.dsplit, torch.vsplit, torch.hsplit, torch.hstack, torch.dstack, torch.vstack, Tensor.conj, torch.add, torch.sub, torch.mul, torch.sub, torch.div, torch.view, torch.view_as, torch.real, torch.imag, torch.neg, Tensor.__getitem__, torch.sum, torch.prod, torch.abs, torch.sgn, torch.exp, torch.log, torch.eq, torch.masked_fill, torch.index_put, torch.rand, torch.randn, torch.full, torch.empty, torch.ones, torch.zeros, torch.block_diag, Tensor.chunk, Tensor.clone, Tensor.contiguous, torch.diag_embed, torch.diagonal, torch.as_strided, torch.column_stack, Tensor.T, Tensor.H, Tensor.mT, Tensor.mH, Tensor.narrow, torch.isfinite, torch.isinf, torch.isreal, torch.flatten, Tensor.chalf, torch.empty_like, torch.movedim` ( [#73847](https://github.com/pytorch/pytorch/pull/73847), [#74667](https://github.com/pytorch/pytorch/pull/74667), [#74854](https://github.com/pytorch/pytorch/pull/74854), [#75010,](https://github.com/pytorch/pytorch/pull/75010)[#75156](https://github.com/pytorch/pytorch/pull/75156), [#75311](https://github.com/pytorch/pytorch/pull/75311), [#75498](https://github.com/pytorch/pytorch/pull/75498), [#76132](https://github.com/pytorch/pytorch/pull/76132), [#76158](https://github.com/pytorch/pytorch/pull/76158), [#75592](https://github.com/pytorch/pytorch/pull/75592), [#76615](https://github.com/pytorch/pytorch/pull/76615), [#77179](https://github.com/pytorch/pytorch/pull/77179), [#77339](https://github.com/pytorch/pytorch/pull/77339), [#77446](https://github.com/pytorch/pytorch/pull/77446), [#77483](https://github.com/pytorch/pytorch/pull/77483), [#77479](https://github.com/pytorch/pytorch/pull/77479), [#77192](https://github.com/pytorch/pytorch/pull/77192), [#76724](https://github.com/pytorch/pytorch/pull/76724), [#77404](https://github.com/pytorch/pytorch/pull/77404)).
* Operators in `torch.fft` now support tensors with `torch.complex32` dtype (CUDA only) ([#74857](https://github.com/pytorch/pytorch/pull/74857)).
* `torch.complex32` tensor now participate in type-promotion ([#76893](https://github.com/pytorch/pytorch/pull/76893))
* Added `torch.chalf` alias for `torch.complex32` and `Tensor.chalf` method ([#75320](https://github.com/pytorch/pytorch/pull/75320)).
* Added proper print support for `torch.chalf` tensors ([#76614](https://github.com/pytorch/pytorch/pull/76614)).
* Added support for complex convolution (data-types supported: `torch.complex32, torch.complex64, torch.complex128`)
    * `torch.nn.functional.conv1d` and `torch.nn.Conv1d` ([#75310](https://github.com/pytorch/pytorch/pull/75310))
    * `torch.nn.functional.conv2d` and `torch.nn.Conv2d` ([#75412](https://github.com/pytorch/pytorch/pull/75412))
    * `torch.nn.functional.conv3d` and `torch.nn.Conv3d` ([#75581](https://github.com/pytorch/pytorch/pull/75581))

## LinAlg

* Added `torch.linalg.ldl_factor_ex` and `torch.linalg.ldl_solve` ([#69828](https://github.com/pytorch/pytorch/pull/69828))
* Added `linalg.vander` ([#76303](https://github.com/pytorch/pytorch/pull/76303))
* Added `linalg.lu` ([#67833](https://github.com/pytorch/pytorch/pull/67833))
* Added `linalg.lu_solve` ([#72935](https://github.com/pytorch/pytorch/pull/72935))

## Meta API

* Added meta tensor kernels for the following operators:
    *  `mse_loss` ([#72294](https://github.com/pytorch/pytorch/pull/72294)), `amax` ([#72124](https://github.com/pytorch/pytorch/pull/72124)), `normal` ([#70089](https://github.com/pytorch/pytorch/pull/70089)) `squeeze()` + `unsqueeze` ([#73440](https://github.com/pytorch/pytorch/pull/73440)), `unfold` ([#75717](https://github.com/pytorch/pytorch/pull/75717)), `clamp_min/max`, ([#76926](https://github.com/pytorch/pytorch/pull/76926)), `index_copy` ([#67329](https://github.com/pytorch/pytorch/pull/67329)), `linalg_cross` ([#72413](https://github.com/pytorch/pytorch/pull/72413)), `amin` ([#73581](https://github.com/pytorch/pytorch/pull/73581))
* Enabled the ability to register Python decompositions for operators as meta kernels, get meta support for `where` and `huber_loss` ([#77353](https://github.com/pytorch/pytorch/pull/77353))
* Registered meta functions through Python for `dot/group_norm/instance_norm/var_mean/index_reduce/matmul/bernoulli/adaptive_avg_pool` ([#77499](https://github.com/pytorch/pytorch/pull/77499))  `index_select/abs/min/max` ([#76916](https://github.com/pytorch/pytorch/pull/76916)), `reflection_pad2d` ([#77681](https://github.com/pytorch/pytorch/pull/77681)), `square` ([#77682](https://github.com/pytorch/pytorch/pull/77682)), `log_sigmoid_forward` ([#77739](https://github.com/pytorch/pytorch/pull/77739)), several more ops ([#77362](https://github.com/pytorch/pytorch/pull/77362))

## torch.nn

* `nn.Dropout1d`: New module for 1D channel-wise dropout ([#79545](https://github.com/pytorch/pytorch/pull/79545))
* `nn.Module`: Public API for stateless / functional module computation ([#75834](https://github.com/pytorch/pytorch/pull/75834))
* `nn.Module`: Support for hooks that run after state dict loading ([#76823](https://github.com/pytorch/pytorch/pull/76823), [#77392](https://github.com/pytorch/pytorch/pull/77392))
* Added support for tensor subclasses as parameters ([#73459](https://github.com/pytorch/pytorch/pull/73459), [#77655](https://github.com/pytorch/pytorch/pull/77655))

## torch.fx

* Core
    * Allowed `Tracer` to record usages of `Buffer`s ([#73612](https://github.com/pytorch/pytorch/pull/73612))
    * Introduced experimental MetaTensorTracer ([#76003](https://github.com/pytorch/pytorch/pull/76003))
    * Introduced `Tracer` the ability to trace different forward functions ([#77502](https://github.com/pytorch/pytorch/pull/77502))

## Composability

* Many features, improvements and fixes to Python tensor subclasses based on `__torch_function__` and  `__torch_dispatch__`
    * Added `__torch_function__` mode, which allows you to override the meaning of all `__torch_function__` overrideable functions within a dynamic scope. ([#75154](https://github.com/pytorch/pytorch/pull/75154))
    * Added `enable_torch_dispatch_mode`, which allows nesting of different `__torch_dispatch__` modes. ([#75965](https://github.com/pytorch/pytorch/pull/75965))
    * Added a default implementation of `__torch_dispatch__` ([#73684](https://github.com/pytorch/pytorch/pull/73684))
    * Added support `super().__torch_dispatch__` with arguments list ([#74509](https://github.com/pytorch/pytorch/pull/74509), [#74720](https://github.com/pytorch/pytorch/pull/74720))
    * Miscellaneous `__torch_function__` fixes ([#75484](https://github.com/pytorch/pytorch/pull/75484), [#75110](https://github.com/pytorch/pytorch/pull/75110))
    * Added `__torch_function__` override protocol supporting to some factory functions ([#75639](https://github.com/pytorch/pytorch/pull/75639))
    * Fixed propagation of warnings when using `__torch_dispatch__`. ([#74357](https://github.com/pytorch/pytorch/pull/74357))
    * Removed spurious warning when using disabled torch function ([#75826](https://github.com/pytorch/pytorch/pull/75826))
    * Added the ability to snapshot TLS for “has-a” use cases of `__torch_dispatch__` ([#72623](https://github.com/pytorch/pytorch/pull/72623), [#74577](https://github.com/pytorch/pytorch/pull/74577))
    * Fixed serialization and deep copying for wrapper subclasses ([#73078](https://github.com/pytorch/pytorch/pull/73078))
    * Allowed `is_contiguous()` to be overridden in `__torch_dispatch__` ([#77906](https://github.com/pytorch/pytorch/pull/77906))
* Added a “functionalization” program transform, that can be used to remove mutation + aliasing ops from PyTorch programs, while maintaining program semantics. Currently while most of the logic for the pass lives in core, the pass is exposed as an API through `functorch`. You can run it with `functorch.experimental.functionalize()`. Example usages can be found [here](https://github.com/pytorch/functorch/blob/130582ce47d30aec58713bb25eb2911b908aa616/test/test_eager_transforms.py#L2909).  ([#75913](https://github.com/pytorch/pytorch/pull/75913), [#76083](https://github.com/pytorch/pytorch/pull/76083), [#76084](https://github.com/pytorch/pytorch/pull/76084), [#73442](https://github.com/pytorch/pytorch/pull/73442), [#77285](https://github.com/pytorch/pytorch/pull/77285),  [#73441](https://github.com/pytorch/pytorch/pull/73441),  [#75302](https://github.com/pytorch/pytorch/pull/75302), [#75818](https://github.com/pytorch/pytorch/pull/75818), [#75819](https://github.com/pytorch/pytorch/pull/75819), [#76125](https://github.com/pytorch/pytorch/pull/76125), [#76318](https://github.com/pytorch/pytorch/pull/76318), [#77358](https://github.com/pytorch/pytorch/pull/77358))
* Added a new `torch.library` API to allow users to override kernels for existing C++ ops through Python ([#75905](https://github.com/pytorch/pytorch/pull/75905), [#76892](https://github.com/pytorch/pytorch/pull/76892))
* Allowed creating new libraries and defining new operators from Python ([#76250](https://github.com/pytorch/pytorch/pull/76250), [#77690](https://github.com/pytorch/pytorch/pull/77690))
* Added experimental API’s for registering and looking up Python decompositions for many aten operators: `from torch._decomp import register_decomposition, get_decompositions`. ([#76311](https://github.com/pytorch/pytorch/pull/76311), [#76814](https://github.com/pytorch/pytorch/pull/76814))
    * Many decompositions have also been added to this table ([#76621](https://github.com/pytorch/pytorch/pull/76621), [#77329](https://github.com/pytorch/pytorch/pull/77329), [#77219](https://github.com/pytorch/pytorch/pull/77219), [#76633](https://github.com/pytorch/pytorch/pull/76633), [#76855](https://github.com/pytorch/pytorch/pull/76855), [#76714](https://github.com/pytorch/pytorch/pull/76714), [#76763](https://github.com/pytorch/pytorch/pull/76763), [#77473](https://github.com/pytorch/pytorch/pull/77473), [#77807](https://github.com/pytorch/pytorch/pull/77807), [#77500](https://github.com/pytorch/pytorch/pull/77500))

## Sparse

* Added factory functions for sparse CSC, BSR, and BSC tensors ([#76634](https://github.com/pytorch/pytorch/pull/76634), [#76623](https://github.com/pytorch/pytorch/pull/76623), [#75946](https://github.com/pytorch/pytorch/pull/75946), [#75961](https://github.com/pytorch/pytorch/pull/75961), [#75831](https://github.com/pytorch/pytorch/pull/75831), [#76651](https://github.com/pytorch/pytorch/pull/76651))
* Added `ccol_indices` and `row_indices` methods for CSC and BSC tensors. ([#77503](https://github.com/pytorch/pytorch/pull/77503))
* Added `to_sparse_csc` with support for 2D Strided and 2D CSC input ([#77521](https://github.com/pytorch/pytorch/pull/77521))
* Added `to_sparse_bsr`  with support for 2D CSR input ([#77366](https://github.com/pytorch/pytorch/pull/77366))
* Added `index_reduce` ([#76997](https://github.com/pytorch/pytorch/pull/76997), [#75981](https://github.com/pytorch/pytorch/pull/75981), [#76296](https://github.com/pytorch/pytorch/pull/76296))

## CUDA

* Add Jiterator support when dtype is complex for `sigmoid`, `exp`, `sqrt`, `rsqrt`, `log`, `log10`, `log2`, `addcmul`, `abs`, `addcdiv`, `sgn`, `neg` , `logical_and`, `angle`([#73643](https://github.com/pytorch/pytorch/pull/73643), [#73776](https://github.com/pytorch/pytorch/pull/73776), [#73781](https://github.com/pytorch/pytorch/pull/73781), [#74160](https://github.com/pytorch/pytorch/pull/74160), [#74161](https://github.com/pytorch/pytorch/pull/74161), [#74533](https://github.com/pytorch/pytorch/pull/74533), [#74455](https://github.com/pytorch/pytorch/pull/74455), [#74827](https://github.com/pytorch/pytorch/pull/74827), [#74814](https://github.com/pytorch/pytorch/pull/74814),  [#74863](https://github.com/pytorch/pytorch/pull/74863), [#75123](https://github.com/pytorch/pytorch/pull/75123),  [#76692](https://github.com/pytorch/pytorch/pull/76692))
* Add Jiterator support when dtype is complex for the backward of `sigmoid` and `tanh `([#76289](https://github.com/pytorch/pytorch/pull/76289), [#74948](https://github.com/pytorch/pytorch/pull/74948))
* Add Jiterator support for `kaiser_window` , `prod` ([#73734](https://github.com/pytorch/pytorch/pull/73734), [#75231](https://github.com/pytorch/pytorch/pull/75231))
* Enable simple reductions with Jiterator ([#75231](https://github.com/pytorch/pytorch/pull/75231))
* Updated to cuDNN v8 API with cuDNN benchmark, convolution bwd / transposed convolution fwd, `bfloat16`, conv-bias-activation fusion ([#60755](https://github.com/pytorch/pytorch/pull/60755))
* Added Python Interface for Jiterator ([#76394](https://github.com/pytorch/pytorch/pull/76394))
* Added Jiterator with Python Registration ([#77121](https://github.com/pytorch/pytorch/pull/77121))
* Prepared Jiterator code template for multiple outputs ([#77902](https://github.com/pytorch/pytorch/pull/77902))
* For CUDA graphs, added `torch.cuda.is_current_stream_capturing` ([#77789](https://github.com/pytorch/pytorch/pull/77789))


## Vulkan

* Added Vulkan support for Gated Recurrent Units (`torch.nn.GRU`) ([#72692](https://github.com/pytorch/pytorch/pull/72692), [#73599](https://github.com/pytorch/pytorch/pull/73599))
* Added Vulkan support for the linear interpolation op (`torch.lerp`) ([#76544](https://github.com/pytorch/pytorch/pull/76544))

## Profiler

* Added support both global (experimental) and thread local profiling ([#75525](https://github.com/pytorch/pytorch/pull/75525), [#76078](https://github.com/pytorch/pytorch/pull/76078), [#76239](https://github.com/pytorch/pytorch/pull/76239))

## Mobile

* Added support for different memory formats of Tensors in NNC ([#72873](https://github.com/pytorch/pytorch/pull/72873))
* Upgraded mobile model bytecode to V9 and provide backporting to previous versions ([#71662](https://github.com/pytorch/pytorch/pull/71662))

## Distributed

* `ShardedTensor` and `tensor parallel` 
    * This is a prototyping effort which consists of having a new class to represent how one `torch.tensor` is being sharded across multiple GPUs or hosts and a high level APIs for users to specify how to shard, enabling basic tensor ops for `ShardedTensor` and enabling optimizer for `ShardedTensor`. In addition, we have added PartialTensor, ReplicatedTensor and checkpoint with ShardedTensor ([#63997](https://github.com/pytorch/pytorch/pull/63997), [#65511](https://github.com/pytorch/pytorch/pull/65511), [#65671](https://github.com/pytorch/pytorch/pull/65671), [#65855](https://github.com/pytorch/pytorch/pull/65855), [#66012](https://github.com/pytorch/pytorch/pull/66012), [#66351](https://github.com/pytorch/pytorch/pull/66351), [#66464](https://github.com/pytorch/pytorch/pull/66464), [#66603](https://github.com/pytorch/pytorch/pull/66603), [#66604](https://github.com/pytorch/pytorch/pull/66604), [#67057](https://github.com/pytorch/pytorch/pull/67057), [#67188](https://github.com/pytorch/pytorch/pull/67188), [#67199](https://github.com/pytorch/pytorch/pull/67199), [#67799](https://github.com/pytorch/pytorch/pull/67799), [#68021](https://github.com/pytorch/pytorch/pull/68021), [#68096](https://github.com/pytorch/pytorch/pull/68096), [#68607](https://github.com/pytorch/pytorch/pull/68607), [#68771](https://github.com/pytorch/pytorch/pull/68771), [#68786](https://github.com/pytorch/pytorch/pull/68786), [#68806](https://github.com/pytorch/pytorch/pull/68806), [#69226](https://github.com/pytorch/pytorch/pull/69226), [#69493](https://github.com/pytorch/pytorch/pull/69493), [#69569](https://github.com/pytorch/pytorch/pull/69569), [#69725](https://github.com/pytorch/pytorch/pull/69725), [#69874](https://github.com/pytorch/pytorch/pull/69874), [#69945](https://github.com/pytorch/pytorch/pull/69945), [#69946](https://github.com/pytorch/pytorch/pull/69946), [#70145](https://github.com/pytorch/pytorch/pull/70145), [#70228](https://github.com/pytorch/pytorch/pull/70228), [#70266](https://github.com/pytorch/pytorch/pull/70266), [#70331](https://github.com/pytorch/pytorch/pull/70331), [#70476](https://github.com/pytorch/pytorch/pull/70476), [#71445](https://github.com/pytorch/pytorch/pull/71445), [#72062](https://github.com/pytorch/pytorch/pull/72062), [#72130](https://github.com/pytorch/pytorch/pull/72130), [#73309](https://github.com/pytorch/pytorch/pull/73309), [#76360](https://github.com/pytorch/pytorch/pull/76360), [#76477](https://github.com/pytorch/pytorch/pull/76477), [#72733](https://github.com/pytorch/pytorch/pull/72733), [#73392](https://github.com/pytorch/pytorch/pull/73392), [#76199](https://github.com/pytorch/pytorch/pull/76199), [#75374](https://github.com/pytorch/pytorch/pull/75374), [#71624](https://github.com/pytorch/pytorch/pull/71624), [#74040](https://github.com/pytorch/pytorch/pull/74040), [#73529](https://github.com/pytorch/pytorch/pull/73529), [#74941](https://github.com/pytorch/pytorch/pull/74941), [#73703](https://github.com/pytorch/pytorch/pull/73703), [#75712](https://github.com/pytorch/pytorch/pull/75712), [#73873](https://github.com/pytorch/pytorch/pull/73873), [#75991](https://github.com/pytorch/pytorch/pull/75991), [#75844](https://github.com/pytorch/pytorch/pull/75844), [#76824](https://github.com/pytorch/pytorch/pull/76824), [#76897](https://github.com/pytorch/pytorch/pull/76897), [#77185](https://github.com/pytorch/pytorch/pull/77185), [#77191](https://github.com/pytorch/pytorch/pull/77191), [#76758](https://github.com/pytorch/pytorch/pull/76758), [#77209](https://github.com/pytorch/pytorch/pull/77209), [#77214](https://github.com/pytorch/pytorch/pull/77214), [#77367](https://github.com/pytorch/pytorch/pull/77367), [#77580](https://github.com/pytorch/pytorch/pull/77580), [#77626](https://github.com/pytorch/pytorch/pull/77626), [#77800](https://github.com/pytorch/pytorch/pull/77800), [#77707](https://github.com/pytorch/pytorch/pull/77707), [#78056](https://github.com/pytorch/pytorch/pull/78056))
        * Design proposal: [ShardedTensor](https://github.com/pytorch/pytorch/issues/55207) and [Sharding APIs](https://github.com/pytorch/pytorch/issues/72138). [Example](https://github.com/pytorch/examples/tree/main/distributed/sharded_tensor) for a Megatron-LM style tensor parallel.
* FullyShardedDataParallel
    * Added `FlatParameter` to track the information of a flat parameter ([#69241](https://github.com/pytorch/pytorch/pull/69241))
    * Enabled `summon_full_params` for FSDP. ([#71225](https://github.com/pytorch/pytorch/pull/71225))
    * Added `no_sync()` context manager ([#72446](https://github.com/pytorch/pytorch/pull/72446))
    * Implemented `apply()` ([#72925](https://github.com/pytorch/pytorch/pull/72925))
    * Implemented local_state_dict and load_local_state_dict ([#73300](https://github.com/pytorch/pytorch/pull/73300))
    * Implemented `full_state_dict` ([#73324](https://github.com/pytorch/pytorch/pull/73324))
    * Implemented `clip_grad_norm` for FSDP ([#73405](https://github.com/pytorch/pytorch/pull/73405))
    * Added grad accumulation without `no_sync()` ([#73535](https://github.com/pytorch/pytorch/pull/73535))
    * Added `full_optim_state_dict` ([#74215](https://github.com/pytorch/pytorch/pull/74215))
    * Implemented `reshard_flatten_tensor` ([#75192](https://github.com/pytorch/pytorch/pull/75192))
    * Added `scatter_full_optim_state_dict()` ([#75517](https://github.com/pytorch/pytorch/pull/75517))
    * Implemented `sharded_state_dict` and `load_sharded_state_dict` ([#77356](https://github.com/pytorch/pytorch/pull/77356))
    * Enabled mixed precision in FSDP ([#75024](https://github.com/pytorch/pytorch/pull/75024))
    * Changed to allow specification of modules to ignore when wrapping with FSDP([#75431](https://github.com/pytorch/pytorch/pull/75431))
    * Added `FullStateDictConfig` to allow full state dict checkpoint with rank0 only and CPU offload ([#75908](https://github.com/pytorch/pytorch/pull/75908))
    * Added validation to ensure FSDP units execute consistently across ranks ([#75902](https://github.com/pytorch/pytorch/pull/75902))
    * Added support for initialization of modules on meta device ([#75880](https://github.com/pytorch/pytorch/pull/75880))
    * Added support for no sharding config for DDP-style parallelism ([#76736](https://github.com/pytorch/pytorch/pull/76736))
    * Changed to allow FSDP to specify device sharded wrapped module should be placed on ([#77321](https://github.com/pytorch/pytorch/pull/77321))
    * Enabled FSDP parameter sync ([#77492](https://github.com/pytorch/pytorch/pull/77492))
    * Made sharding strategy configurable and support zero2 algorithm ([#73819](https://github.com/pytorch/pytorch/pull/73819))
    * Added a shard aware grad scaler for FSDP+MixedPrecision ([#76918](https://github.com/pytorch/pytorch/pull/76918))
    * Enabled FSDP full state dict to work for non root FSDP modules via post load hooks ([#76912](https://github.com/pytorch/pytorch/pull/76912))
    * Added `always_wrap` policy ([#73687](https://github.com/pytorch/pytorch/pull/73687))
    * Provided an auto wrap policy for common transformer models ([#76455](https://github.com/pytorch/pytorch/pull/76455))
* DistributedDataParallel
    * Added support for hierarchical model averaging ([#73285](https://github.com/pytorch/pytorch/pull/73285))
* torch.distributed.rpc
    * Changed to allow for optional `world_size` argument in `init_rpc` ([#73372](https://github.com/pytorch/pytorch/pull/73372))
    * Changed to allow newly joined ranks to communicate with existing ranks ([#73373](https://github.com/pytorch/pytorch/pull/73373))
    * Changed to allow existing ranks to communicate with newly joined ranks ([#74035](https://github.com/pytorch/pytorch/pull/74035))
    * Added graceful shutdown for dynamic RPC members ([#74561)](https://github.com/pytorch/pytorch/pull/74561)

## JIT/TorchScript

* Added autocasting of values from fp32 to lower precision floats in `torch.jit.freeze`  ([#74178](https://github.com/pytorch/pytorch/pull/74178))
* `torch.jit.set_fusion_strategy` is now a public API, allowing one to set if they want fusion based on static or dynamic tensor sizes ([#72639](https://github.com/pytorch/pytorch/pull/72639))
* Added support for compiling `tensor.__getitem__()` ([#73952](https://github.com/pytorch/pytorch/pull/73952))
* TorchScript uses a fuser to combine multiple operator calls into a single kernel. In 1.12 the default fuser for NVIDIA GPUs is switched to NVFuser, which supports a wider range of operators and has demonstrated improved throughput compared to NNC, the previous fuser. ([#74361](https://github.com/pytorch/pytorch/pull/74361), [#77010](https://github.com/pytorch/pytorch/pull/77010), [#77395](https://github.com/pytorch/pytorch/pull/77395), [#72127](https://github.com/pytorch/pytorch/pull/72127), [#73627](https://github.com/pytorch/pytorch/pull/73627), [#75235](https://github.com/pytorch/pytorch/pull/75235), [#75539](https://github.com/pytorch/pytorch/pull/75539), [#75558](https://github.com/pytorch/pytorch/pull/75558), [#75646](https://github.com/pytorch/pytorch/pull/75646), [#76226](https://github.com/pytorch/pytorch/pull/76226), [#76459](https://github.com/pytorch/pytorch/pull/76459), [#76604](https://github.com/pytorch/pytorch/pull/76604), [#76563](https://github.com/pytorch/pytorch/pull/76563), [#77001](https://github.com/pytorch/pytorch/pull/77001), [#77017](https://github.com/pytorch/pytorch/pull/77017), [#77471](https://github.com/pytorch/pytorch/pull/77471), [#77777](https://github.com/pytorch/pytorch/pull/77777), [#77884](https://github.com/pytorch/pytorch/pull/77884), [#76790](https://github.com/pytorch/pytorch/pull/76790), [#76343](https://github.com/pytorch/pytorch/pull/76343), [#76605](https://github.com/pytorch/pytorch/pull/76605), [#76769](https://github.com/pytorch/pytorch/pull/76769), [#77158](https://github.com/pytorch/pytorch/pull/77158), [#74339](https://github.com/pytorch/pytorch/pull/74339))
* Added option to save extra files in `torch.jit.save_jit_module_to_flatbuffer` ([#77870](https://github.com/pytorch/pytorch/pull/77870))

## Quantization

* Added oneDNN quantization backend ([#69820](https://github.com/pytorch/pytorch/pull/69820))
* Added oneDNN quant backend ([#74137](https://github.com/pytorch/pytorch/pull/74137))

## ONNX

* Added support to exporting additional ops: 
    * `Cross`, `Cdist` and `Pairwise Distance` ([#75278](https://github.com/pytorch/pytorch/pull/75278))
    * `bucketize` ([#74856](https://github.com/pytorch/pytorch/pull/74856))
    * `pixel unshuffle` ([#72499](https://github.com/pytorch/pytorch/pull/72499))
    * `embedding_renorm` ([#72738](https://github.com/pytorch/pytorch/pull/72738))
    * `aminmax` ([#75714](https://github.com/pytorch/pytorch/issues/75714))
    * `amax` and `amin` ([#75268](https://github.com/pytorch/pytorch/pull/75268))
    * `grid_sample` ([#76159](https://github.com/pytorch/pytorch/issues/76159))
* Added support to exporting quantized models ([#72986](https://github.com/pytorch/pytorch/issues/72986), [#73102](https://github.com/pytorch/pytorch/issues/73102), [#75697,](https://github.com/pytorch/pytorch/pull/75697) [#76002,](https://github.com/pytorch/pytorch/pull/76002) [#76055,](https://github.com/pytorch/pytorch/pull/76055) [#73336,](https://github.com/pytorch/pytorch/pull/73336)[#77393,](https://github.com/pytorch/pytorch/pull/77393) [#75920,](https://github.com/pytorch/pytorch/pull/75920) [#75921](https://github.com/pytorch/pytorch/pull/75921))
* Added support to optional type. See tests in PR for examples. ([#73284](https://github.com/pytorch/pytorch/issues/73284))
* Added support to ATen fallback for non-Caffe2 implementations of ONNX ([#74759](https://github.com/pytorch/pytorch/pull/74759), [#75468,](https://github.com/pytorch/pytorch/pull/75468) [#74680,](https://github.com/pytorch/pytorch/pull/74680) [#73954](https://github.com/pytorch/pytorch/pull/73954))

## Infra (Releng)

* Added support for ROCm 5.0 ([#72895](https://github.com/pytorch/pytorch/pull/72895))
* Added LibTorch builds for ROCm ([#57506](https://github.com/pytorch/pytorch/pull/57506))
* Added support for CUDA 11.6 ([#75518](https://github.com/pytorch/pytorch/pull/75518))

# Improvements

## Python API

* Improved numerical stability of `torch.distributions.wishart.Wishart` ([#72993](https://github.com/pytorch/pytorch/pull/72993))
* Added `mode` property to `torch.distributions.Distribution` ([#76690](https://github.com/pytorch/pytorch/pull/76690))
* Added `foreach` flag for `torch.optim.{Adadelta, Adagrad, Adamax, Adam, ASGD, NAdam, RAdamSGD, Rmsprop, Rprop, AdamW}` ([#69980](https://github.com/pytorch/pytorch/pull/69980), [#69981](https://github.com/pytorch/pytorch/pull/69981), [#69982](https://github.com/pytorch/pytorch/pull/69982), [#70295](https://github.com/pytorch/pytorch/pull/70295), [#70481](https://github.com/pytorch/pytorch/pull/70481), [#70229](https://github.com/pytorch/pytorch/pull/70229), [#70230](https://github.com/pytorch/pytorch/pull/70230), [#70231](https://github.com/pytorch/pytorch/pull/70231), [#70482](https://github.com/pytorch/pytorch/pull/70482), [#70483](https://github.com/pytorch/pytorch/pull/70483), [#70484](https://github.com/pytorch/pytorch/pull/70484))
* Added out variant for `torch.softmax` and `torch.log_softmax` ([#75833](https://github.com/pytorch/pytorch/pull/75833))
* Added handling for r=0 case for `torch.combinations` ([#70270](https://github.com/pytorch/pytorch/pull/70270))
* Added XPU support for `torch.autocast` ([#75250](https://github.com/pytorch/pytorch/pull/75250))
* Added support for Tensor source for `.set_(storage, offset, size, strides)` ([#77007](https://github.com/pytorch/pytorch/pull/77007))
* Changed to register `torch.return_types.*` as pytree nodes ([#75915](https://github.com/pytorch/pytorch/pull/75915))
* Added typing for `torch.return_type` ([#74199](https://github.com/pytorch/pytorch/pull/74199))
* Set correct module for APIs in the `torch` module ([#75801](https://github.com/pytorch/pytorch/pull/75801))
* Improved `NotImplementedError` verbosity for `torch.distributions.kl_divergence` ([#72845](https://github.com/pytorch/pytorch/pull/72845))
* Added maximize flag to `torch.optim.Adagrad` ([#75968](https://github.com/pytorch/pytorch/pull/75968))
* `optim.{Adagrad, Adam, Adamax, AdamW, RAdam}`: Updated `step` in functional optimizers and pass `state_steps` instead of `state` ([#71333](https://github.com/pytorch/pytorch/pull/71333))
* Improved `torch.lerp` numerical precision by doing intermediate math in opmath_t ([#76062](https://github.com/pytorch/pytorch/pull/76062))
* Changed to alias `torch.finfo.tiny` to `torch.finfo.smallest_normal` ([#76292](https://github.com/pytorch/pytorch/pull/76292))

## C++ API

* Added catch for overflows in calculating storage byte size for `col2im `([#73719](https://github.com/pytorch/pytorch/pull/73719))
* Implemented center padding for `stft` ([#73432](https://github.com/pytorch/pytorch/pull/73432))

## Autograd

* Added forward AD support for `torch.{atan2, dist, logsumexp, log_softmax, norm, polar, put softmax}` ([#73741](https://github.com/pytorch/pytorch/pull/73741), [#74205](https://github.com/pytorch/pytorch/pull/74205), [#75027](https://github.com/pytorch/pytorch/pull/75027), [#75326](https://github.com/pytorch/pytorch/pull/75326), [#77421](https://github.com/pytorch/pytorch/pull/77421))
* Added forward AD support for `torch.nn.functional.{cross_entropy, pairwise_dist, nll_loss, normalize}` ([#73741](https://github.com/pytorch/pytorch/pull/73741), [#74205](https://github.com/pytorch/pytorch/pull/74205))
* Added forward AD support for `torch.cholesky_inverse` ([#75033](https://github.com/pytorch/pytorch/pull/75033))
* Added forward AD and forward-over-reverse support for FFTs ([#75326](https://github.com/pytorch/pytorch/pull/75326))
* Added forward AD support for `torch.nn.functional.{embedding,prelu, bilinear, rrelu, logsigmoid}` ([#77421](https://github.com/pytorch/pytorch/pull/77421))
* Added forward AD support for `torch.nn.BCELoss` ([#77755](https://github.com/pytorch/pytorch/pull/77755))
* Added forward AD support for `Tensor.__rsub__` ([#75326](https://github.com/pytorch/pytorch/pull/75326))
* Added forward AD support for `torch.clamp` when bounds are tensors ([#74042](https://github.com/pytorch/pytorch/pull/74042))
* Added forward AD support for `torch.nn.functional.{dropout, glu}`([#75288](https://github.com/pytorch/pytorch/pull/75288), [#77186](https://github.com/pytorch/pytorch/pull/77186))
* Added forward-over-reverse for `torch.nn.functional.`{`leaky_relu, glu, elu, selu, celu}` ([#75294](https://github.com/pytorch/pytorch/pull/75294), [#77309](https://github.com/pytorch/pytorch/pull/77309), [#75297](https://github.com/pytorch/pytorch/pull/75297))
* Improved forward and backward derivative `torch.{linalg.cholesky, cholesky}` ([#76032](https://github.com/pytorch/pytorch/pull/76032))
* Improved forward and backward derivative of `torch.linalg.qr` ([#76115](https://github.com/pytorch/pytorch/pull/76115))
* Added complex autograd support for  `torch.cholesky_inverse` ([#75033](https://github.com/pytorch/pytorch/pull/75033))
* Added double backward support for `torch.nn.functional.binary_cross_entropy` wrt target ([#77416](https://github.com/pytorch/pytorch/pull/77416))
* Improved error message for `torch.nn.functional.batch_norm` when `running_{mean,var}` have forward grad defined ([#73655](https://github.com/pytorch/pytorch/pull/73655))
* Improve error message when forward AD is not supported ([#75105](https://github.com/pytorch/pytorch/pull/75105))
* Added forward AD and forward-over-reverse support for `torch.nn.functional.max_unpool` ([#68625](https://github.com/pytorch/pytorch/pull/68625))
* Added autograd support for `masked_softmax` ([#71502](https://github.com/pytorch/pytorch/pull/71502))

## Build

* Fixed pybind deprecation warnings ([#72376](https://github.com/pytorch/pytorch/pull/72376))
* Enabled win-arm64 ([#72424](https://github.com/pytorch/pytorch/pull/72424))
* Moved magma utils to its own header ([#73058](https://github.com/pytorch/pytorch/pull/73058))
* Turned on -Wsign-compare ([#74996](https://github.com/pytorch/pytorch/pull/74996))
* Made all `.pyi.in` files exportable from torch/_C/ folder ([#74962](https://github.com/pytorch/pytorch/pull/74962))
* Improved Jinja2 for docs/cpp build set to version 3.0 ([#74718](https://github.com/pytorch/pytorch/pull/74718))
* Added CMake option for using static MKL libraries ([#73069](https://github.com/pytorch/pytorch/pull/73069))
* CPU Kernel: Changed to use per-operator headers ([#71137](https://github.com/pytorch/pytorch/pull/71137))
* CUDA Kernels: Changed to use per-operator headers ([#71212](https://github.com/pytorch/pytorch/pull/71212))

## Dataloader

* Added `pin_memory_device` to Dataloader to pin `Tensor` to the corresponding GPU device ([#65402](https://github.com/pytorch/pytorch/pull/65402))

## ForEach

* Improved numerical precision for `ForEach` L1 and L2 norm by using  `OpMathType` tensor for intermediate results ([#68107](https://github.com/pytorch/pytorch/pull/68107))

## Meta API

* Changed to skip superfluous storage allocations while constructing meta tensors ([#65331](https://github.com/pytorch/pytorch/pull/65331))

## torch.nn

* Made `nn.init.orthogonal_` no-op for empty input ([#75553](https://github.com/pytorch/pytorch/pull/75553))
* `nn.{Conv1d, Conv2d, Conv3d}`: Added support for complex datatypes ([#75310](https://github.com/pytorch/pytorch/pull/75310), [#75412](https://github.com/pytorch/pytorch/pull/75412), [#75581](https://github.com/pytorch/pytorch/pull/75581))
* `nn.Conv2d`: Added bfloat16 support for mkl-dnn backend ([#55864](https://github.com/pytorch/pytorch/pull/55864))
* `nn.Conv2d`: Added support for channels last memory format on CPU for mkl-dnn backend, naive algorithm, and dilated algorithm ([#55584](https://github.com/pytorch/pytorch/pull/55584), [#68101](https://github.com/pytorch/pytorch/pull/68101), [#70665](https://github.com/pytorch/pytorch/pull/70665))
* `nn.EmbeddingBag`: Added half precision support on CPU ([#74844](https://github.com/pytorch/pytorch/pull/74844))
* `nn.FractionalMaxPool*d`: Added support `0`s in `out_size` ([#73634](https://github.com/pytorch/pytorch/pull/73634))
* `nn.Module`: Changed to throw error for non-dict inputs to `load_state_dict()` ([#77197](https://github.com/pytorch/pytorch/pull/77197))
* `nn.{PixelShuffle, PixelUnshuffle}`: Added support for channels last memory format ([#50573](https://github.com/pytorch/pytorch/pull/50573))
* `nn.PReLU`: Enabled fp32/bfloat16 forward and backward for mkl-dnn backend ([#60427](https://github.com/pytorch/pytorch/pull/60427))
* `F.elu`: Improve numerical precision by using `opmath` and `expm1` ([#77062](https://github.com/pytorch/pytorch/pull/77062))
* `F.{hardshrink, hardsigmoid, hardswish, logsigmoid,  smooth_l1_loss, softplus, softshrink}, nn.{BatchNorm, GLU, Upsample}`: Add bfloat16 support on CPU ([#62558](https://github.com/pytorch/pytorch/pull/62558), [#63134](https://github.com/pytorch/pytorch/pull/63134), [#77496](https://github.com/pytorch/pytorch/pull/77496), [#61944](https://github.com/pytorch/pytorch/pull/61944), [#76935](https://github.com/pytorch/pytorch/pull/76935))

## torch.fx

* FX/graph_drawer
    * Added args/kwargs and users ([#73464](https://github.com/pytorch/pytorch/pull/73464))
    * Added `skip_node_names_in_args` option, default to `True` ([#73815](https://github.com/pytorch/pytorch/pull/73815))
* Core
    * Refactor FX codegen into extensible Codegen object ([#72566](https://github.com/pytorch/pytorch/pull/72566))
    * Modified `replace_all_uses_with` to allowing filtering of nodes to update([#73763](https://github.com/pytorch/pytorch/pull/73763))
    * Made `immutable_list` and `immutable_dict` work with pytrees ([#73766](https://github.com/pytorch/pytorch/pull/73766))
    * Added `Assert None concrete_args` and improve error messages ([#74662](https://github.com/pytorch/pytorch/pull/74662))
* In minimizer, made args work in the `uru10x10_to_trt_eval` script ([#74707](https://github.com/pytorch/pytorch/pull/74707))
* For split_module, changed to return mapping of qualified names from split_module() ([#73564](https://github.com/pytorch/pytorch/pull/73564))
* For shape propagation, made shapes and args/kwargs concrete for minimizer ([#75291](https://github.com/pytorch/pytorch/pull/75291))

## Sparse

* Added CUDA support for `scatter_reduce` ([#74606,](https://github.com/pytorch/pytorch/pull/74606)[#74607](https://github.com/pytorch/pytorch/pull/74607))
* Added 2D Strided, 2D CSR, 2D CSC, 2D COO support to `to_sparse_csr` ([#77521](https://github.com/pytorch/pytorch/pull/77521))
* Added ND Strided, 2D CSC support to `to_dense` ([#74486](https://github.com/pytorch/pytorch/pull/74486), [#77521](https://github.com/pytorch/pytorch/pull/77521))
* Added 2D CSC support to `to_sparse`  ([#73642](https://github.com/pytorch/pytorch/pull/73642), [#77521](https://github.com/pytorch/pytorch/pull/77521))
* Added support for batched CSR to `sparse_csr_tensor` ([#74542](https://github.com/pytorch/pytorch/pull/74542))
* Added support for `__str__` for CSC, BSR, and BSC tensors ([#77530](https://github.com/pytorch/pytorch/pull/77530), [#76650](https://github.com/pytorch/pytorch/pull/76650))
* Updated transpose to return CSC when given CSR ([#77615](https://github.com/pytorch/pytorch/pull/77615))
* Added support for CSR gradients for CSR tensors ([#75435](https://github.com/pytorch/pytorch/pull/75435))
* Added CSC support to `addmm`, `addmv`, `mm` ([#77615](https://github.com/pytorch/pytorch/pull/77615))
* Added autograd for CSR inputs to `torch.sparse.sampled_addmm` ([#68084](https://github.com/pytorch/pytorch/pull/68084))
* Added autograd for CSR inputs to `torch.sparse.addmm and torch.sparse.mm` ([#76591](https://github.com/pytorch/pytorch/pull/76591))
* Added Half/BFloat16 support for to_dense and coalesce methods. ([#72397](https://github.com/pytorch/pytorch/pull/72397))
* Added CSR support to `mul` ([#74266](https://github.com/pytorch/pytorch/pull/74266), [#77177](https://github.com/pytorch/pytorch/pull/77177))
* Added CSR support to `sum` ([#74766](https://github.com/pytorch/pytorch/pull/74766))
* Added BSR support to `addmm`, `addmv`, `triangular_solve` ([#77255](https://github.com/pytorch/pytorch/pull/77255))
* Added batched CSR support to `torch.sparse.sampled_addmm` on CUDA ([#77243](https://github.com/pytorch/pytorch/pull/77243))
* Added CSR support for `torch.sparse.sampled_addmm` on CPU ([#76589](https://github.com/pytorch/pytorch/pull/76589))
* Added CSR support to `torch.select` ([#76228](https://github.com/pytorch/pytorch/pull/76228))
* Added CSR support to `Tensor.to` ([#76400](https://github.com/pytorch/pytorch/pull/76400))
* Added CSC support to `torch.empty` ([#77508](https://github.com/pytorch/pytorch/pull/77508))
* Added CSC, BSR, BSC support to `torch.clone` ([#77512](https://github.com/pytorch/pytorch/pull/77512))
* Added CSC, BSR, BSC support for `copy_`  ([#77605](https://github.com/pytorch/pytorch/pull/77605))
* Added (Strided, CSR) input support to `torch.mm` ([#73686](https://github.com/pytorch/pytorch/pull/73686))
* Added CSR support to `torch.sparse.mm` ([#73075](https://github.com/pytorch/pytorch/pull/73075))
* Added (Strided, CSR, CSR) support to `addmm` on CPU ([#73076](https://github.com/pytorch/pytorch/pull/73076))
* Added runtime beta support warning to CSR, CSC, BSR, BSC tensors ([#75594](https://github.com/pytorch/pytorch/pull/75594), [#75865](https://github.com/pytorch/pytorch/pull/75865))
* Added `bool` support to `coalesce` and `to_dense`  ([#74495](https://github.com/pytorch/pytorch/pull/74495))
* Added `half` support to `sparse_mask` ([#76862](https://github.com/pytorch/pytorch/pull/76862))
* Added AMD Navi 21 support to `coalesce` ([#73548](https://github.com/pytorch/pytorch/pull/73548))

## AMD

* Enabled `atomicAddNoRet()` for all gfx targets. ([#75451](https://github.com/pytorch/pytorch/pull/75451))
* Enabled miopen for RNNs with dropout. ([#75429](https://github.com/pytorch/pytorch/pull/75429))
* Used `ncclAllToAll` for ROCm ([#75128](https://github.com/pytorch/pytorch/pull/75128))
* Navi21 Enablement: fix TI `num_threads` for ROCm,  Depthwise kernels, Embedding kernels, Normalization kernels, Softmax kernels, Tensor kernels, Index, Repeat and Sort kernels, Range and Multinomial Kernels ([#69942](https://github.com/pytorch/pytorch/pull/69942), [#72682](https://github.com/pytorch/pytorch/pull/72682), [#72809](https://github.com/pytorch/pytorch/pull/72809), [#73543](https://github.com/pytorch/pytorch/pull/73543),  [#73545](https://github.com/pytorch/pytorch/pull/73545), [#73546](https://github.com/pytorch/pytorch/pull/73546), [#73549](https://github.com/pytorch/pytorch/pull/73549), [#73550](https://github.com/pytorch/pytorch/pull/73550))
* Added ROCm version api within CMake ([#69481](https://github.com/pytorch/pytorch/pull/69481))
* Enabled `sort` operator BF16 support ([#72854](https://github.com/pytorch/pytorch/pull/72854))
* Enabled HIP IPC ([#74383](https://github.com/pytorch/pytorch/pull/74383))
* Enabled `topk` operator for `bfloat16` dtype ([#71913](https://github.com/pytorch/pytorch/pull/71913))
* Added HIP_HOME/include.lib in cpp_extensions ([#75548](https://github.com/pytorch/pytorch/pull/75548))

## CUDA

* PyTorch: added support to NVTX range_start and range_end ([#70030](https://github.com/pytorch/pytorch/pull/70030))
* Show friendly error message when forgetting `init` in `torch.cuda` ([#72404](https://github.com/pytorch/pytorch/pull/72404))
* PyTorch GPU Allocator: better use of blocks with rounding of allocation sizes ([#74213](https://github.com/pytorch/pytorch/pull/74213))
* CUDACachingAlloc/GPUInference: implemented garbage collection without GPU sync ([#74261](https://github.com/pytorch/pytorch/pull/74261))
* CUBLAS/TF32: added environment variable to allow override of `allow_tf32_cublas` ([#77114](https://github.com/pytorch/pytorch/pull/77114))

## Intel 

* Bfloat16
  * Added BFloat16 support for `torch.{nn.PReLU, nn.Upsample,nn.GLU, randperm, multinomial, poisson, nn.ELU, nn.SELU, nn.CELU, nn.LogSigmoid, nn.Hardsigmoid, nn.Hardshrink, nn.Softshrink, nn.Hardswish, nn.Softplus, nn.SmoothL1Loss, histc, atan2, logcumsumexp, diag, fmod, cumsum, cumprod, nn.utils.weight_norm , nn.BatchNorm2d}` and allow autocast enabled ([_#63634,_](https://github.com/pytorch/pytorch/pull/63634) [_#58297,_](https://github.com/pytorch/pytorch/pull/58297) [_#61944,_](https://github.com/pytorch/pytorch/pull/61944) [_#63215 ,_](https://github.com/pytorch/pytorch/pull/63215) [_#62546,_](https://github.com/pytorch/pytorch/pull/62546) [_#63134_](https://github.com/pytorch/pytorch/pull/63134), [_#72694,_](https://github.com/pytorch/pytorch/pull/72694) [_#61897,_](https://github.com/pytorch/pytorch/pull/61897) [_#73845,_](https://github.com/pytorch/pytorch/pull/73845) [_#74410,_](https://github.com/pytorch/pytorch/pull/74410) [_#68725_](https://github.com/pytorch/pytorch/pull/68725))
    * Improved `torch.nn.functional.log_softmax` on CPU when dim != -1 on both float32 and bfloat16 ([_#64726_](https://github.com/pytorch/pytorch/pull/64726))
    * Improved `torch.nn.functional.layer_norm` bfloat16 performance on CPU ([_#71376_](https://github.com/pytorch/pytorch/pull/71376))
    * Improved autocast cpu documentation ([_#68567_](https://github.com/pytorch/pytorch/pull/68567))
* Channels last
    * Add channels-last support for `torch.nn.{conv2D(kernel slow_conv_dilated2d and thnn_conv2d, mkldnn as backend), GroupNorm, PixelShuffle, PixelUnshuffle}`([_#70665_](https://github.com/pytorch/pytorch/pull/70665), [_#68101_](https://github.com/pytorch/pytorch/pull/68101), [_#55584,_](https://github.com/pytorch/pytorch/pull/55584) [_#50573,_](https://github.com/pytorch/pytorch/pull/50573) [_#555864_](https://github.com/pytorch/pytorch/pull/555864))
* OneDNN
    * Upgraded oneDNN to v2.6.0, ([_#75398_](https://github.com/pytorch/pytorch/pull/75398))
    * Added JIT graph fuser for oneDNN Graph API (v0.5) ([_#76622_](https://github.com/pytorch/pytorch/pull/76622))
* Quantization
    * Improve {`qcat_nhwc, qupsample_bilinear2d, qupsample_nearest2d, qbatch_norm2d, qmax_pool2d, qavg_pool2d`} performance on multi-core ([_#69667_](https://github.com/pytorch/pytorch/pull/69667), [_#69601_](https://github.com/pytorch/pytorch/pull/69601), [_#69600,_](https://github.com/pytorch/pytorch/pull/69600) [_#69599_](https://github.com/pytorch/pytorch/pull/69599), [_#69598_](https://github.com/pytorch/pytorch/pull/69598), [_#69517_](https://github.com/pytorch/pytorch/pull/69517))
    * Add oneDNN as backend for quantization ([_#69820_](https://github.com/pytorch/pytorch/pull/69820)) 
* Improved `torch{norm,argmax,argmin, scatter, gather}` performance on CPU ([_#64479_](https://github.com/pytorch/pytorch/pull/64479), [_#64478_](https://github.com/pytorch/pytorch/pull/64478))
* Improved `torch.nn.functional{log_softmax``, softmax}` performance on CPU ([_#73953_](https://github.com/pytorch/pytorch/pull/73953))
* Expanded graph rewrite to handle `conv_transpose3d` ([_#76888_](https://github.com/pytorch/pytorch/pull/76888))
* Expanded coverage of convolution folding in conv→mul→add→bn ([_#75724_](https://github.com/pytorch/pytorch/pull/75724))
* Added MKLDNN support for `PReLU` ([_#60427_](https://github.com/pytorch/pytorch/pull/60427))

## Composability 

* Added `torch.nn.init` to list of functions overridable by `__torch_function__` ([#76014](https://github.com/pytorch/pytorch/pull/76014))
* Relaxed dtype restrictions on `torch.Tensor`([#73850](https://github.com/pytorch/pytorch/pull/73850))

## Profiler

* Enabled iteration tracking for kineto ([#72292](https://github.com/pytorch/pytorch/pull/72292))
* Added support for input sequence ID tracking for NVTX profiler ([#70264](https://github.com/pytorch/pytorch/pull/70264))
* Re-enabled user-annotations in PyTorch ([#75601](https://github.com/pytorch/pytorch/pull/75601))
* Added support to configure Kineto CUPTI profiler from PyTorch profiler interface ([#75616](https://github.com/pytorch/pytorch/pull/75616))

## Vulkan

* Added an interface to obtain execution time data for GPU shader kernels when executing Vulkan operators ([#75829](https://github.com/pytorch/pytorch/pull/75829))

## Mobile

* Improved Android instrumentation test and update README ([#72736](https://github.com/pytorch/pytorch/pull/72736))
* Improved unsupported scalar type error message for Android ([#74660](https://github.com/pytorch/pytorch/pull/74660))



## JIT/TorchScript

* `torch.jit.trace` now treats `tensor.numel()` as `aten::numel`, instead of a constant value ([#74081](https://github.com/pytorch/pytorch/pull/74081))
* When printing out the types of a JIT Dict, with a tuple key, we now print out the types of the tuple if it is simple ([#76164](https://github.com/pytorch/pytorch/pull/76164))
* Added support for basic ops support for complex numbers in JIT, We now support op(complex, Tensor) for the following: add (+), mul (*), eq (==), ne (!=), sub (-), div (/) ([#73286](https://github.com/pytorch/pytorch/pull/73286))
* TorchScript now preserves the original exception message when rethrowing a Python-based exception ([#77093](https://github.com/pytorch/pytorch/pull/77093))
* Modified the conditions for conv folding in `torch.jit.freeze` to allow for folding arguments that can be promoted to floating point (eg integer tensor arguments) ([#73278](https://github.com/pytorch/pytorch/pull/73278))
* Reduced size of JIT debug.pkl files by only storing unique traces ([#76688](https://github.com/pytorch/pytorch/pull/76688))
* `torch.jit.save` and `torch.jit.load` are now supported for meta tensors ( aka `torch.Tensor(device="meta")`) ([#73435](https://github.com/pytorch/pytorch/pull/73435))

## Architecture Optimization

* Added default symmetric qconfig for QNNPACK ([#74396](https://github.com/pytorch/pytorch/pull/74396))

## Quantization

* Core (Quantized Tensor, Operator, Modules)
    * Added QAT fused `Linear-Bn1d` ([#72431](https://github.com/pytorch/pytorch/pull/72431), [#72796](https://github.com/pytorch/pytorch/pull/72796))
    * Added 4 bit support for embedding quantized module (re-land PR 69769) ([#72276](https://github.com/pytorch/pytorch/pull/72276))
    * Enabled slicing on per-channel quantized tensors (support is limited to the a contiguous sliced tensor) and corresponding test case ([#71269](https://github.com/pytorch/pytorch/pull/71269))
    * Added `qint32` quantization support ([#72472](https://github.com/pytorch/pytorch/pull/72472))
    * Added explicit entries for for functional and module conv and linear support into `get_default_qconfig_dict`&`get_default_qat_qconfig_dict` ([#73528](https://github.com/pytorch/pytorch/pull/73528))
    * Added default symmetric QAT qconfig for QNNPACK ([#74507](https://github.com/pytorch/pytorch/pull/74507))
    * Added Quantized `Matmul` Op (Naive Implementation) ([#71783](https://github.com/pytorch/pytorch/pull/71783))
    * Added Quantized `Softmax` Op (Naive Implementation) ([#75415](https://github.com/pytorch/pytorch/pull/75415))
    * Using QNNPACK in Quantized `Softmax` Op ([#75799](https://github.com/pytorch/pytorch/pull/75799))
* Eager Mode Quantization
    * Added 4 bit support for eager mode quantization flow ([#72277](https://github.com/pytorch/pytorch/pull/72277))
* FX Graph Mode Quantization
    * Added workflow support for `torch.matmul` quantization ([#72444](https://github.com/pytorch/pytorch/pull/72444))
    * Added support `conv1d` and its fusion variants in QAT ([#74506](https://github.com/pytorch/pytorch/pull/74506))
    * Decoupled `prepare_*fx `from training/eval modes ([#75401](https://github.com/pytorch/pytorch/pull/75401))
    * Added quantized Softmax workflow integration ([#75106](https://github.com/pytorch/pytorch/pull/75106))
    * Renamed `default_affine_fixed_qparams_observer` and `default_symmetric_fixed_qparams_observer` ([#76637](https://github.com/pytorch/pytorch/pull/76637))

## ONNX

* Updated default `opset_version` to 13. The previous default was 9. To get the old behavior, just specify `opset_version=9` when calling ``torch.onnx.export``. Going forward we plan to update the default regularly to "latest as of 18 months ago". ([#73898](https://github.com/pytorch/pytorch/issues/73898))
* De-duplicated initializers to reduce ONNX model size for shared parameters ([#69547,](https://github.com/pytorch/pytorch/pull/69547) [#74247](https://github.com/pytorch/pytorch/pull/74247))
* Changed to capture annotated attributes for local function ([#72883](https://github.com/pytorch/pytorch/pull/72883))
* Improve error and warning messages ([#71342,](https://github.com/pytorch/pytorch/pull/71342) [#73255,](https://github.com/pytorch/pytorch/pull/73255) [#73770,](https://github.com/pytorch/pytorch/pull/73770) [#73265](https://github.com/pytorch/pytorch/pull/73265))
* Added support to exporting `torch.minimum` with different dtype combinations ([#76022](https://github.com/pytorch/pytorch/issues/76022)) 
* Improved `Expand` shape inference ([#72985](https://github.com/pytorch/pytorch/pull/72985))
* Added broadcast to `matmul` shape inference ([#72990](https://github.com/pytorch/pytorch/pull/72990))
* Rewrote linspace symbolic to improve numerical stability ([#73610](https://github.com/pytorch/pytorch/pull/73610))
* Enabled `topk` export with non-int64 k ([#73761](https://github.com/pytorch/pytorch/pull/73761))
* Enabled `numel` tracing ([#74081](https://github.com/pytorch/pytorch/pull/74081))
* Added constant folding for `onnx::ReduceProd` ([#74082](https://github.com/pytorch/pytorch/pull/74082))
* Added support to equality checks on devices ([#77203](https://github.com/pytorch/pytorch/issues/77203))
* Added support to dynamic dimensions in `Squeeze` and `Unsqueeze` ([#73104](https://github.com/pytorch/pytorch/pull/73104))

## torch.package

* Added Python Version to `Torch.Package` metadata ([#74610](https://github.com/pytorch/pytorch/pull/74610))
* Added utility for determining where bad modules may come from ([#74998](https://github.com/pytorch/pytorch/pull/74998))

## Distributed

* torch.distributed
    * Refactored `TORCH_DISTRIBUTED_DEBUG` implementation ([#73166](https://github.com/pytorch/pytorch/pull/73166))
    * Set default value of TCPStore world_size to None in pybind definition ([#77277](https://github.com/pytorch/pytorch/pull/77277))
    * Added orthogonalization with QR factorization ([#72043](https://github.com/pytorch/pytorch/pull/72043))
    * Added pickling support for WorkerInfo ([#73371](https://github.com/pytorch/pytorch/pull/73371))
    * Added support for RRefs that contain `threading.Thread` ([#74462](https://github.com/pytorch/pytorch/pull/74462))
    * Added check for mismatch in number of parameters in `verify_params_across_processes` ([#74113](https://github.com/pytorch/pytorch/pull/74113))
    * Added support for backend to register reducer timer ([#71700](https://github.com/pytorch/pytorch/pull/71700))
    * Made ProcessGroupNCCL load torch_ucc.so when TORCH_UCC_LIBRARY_PATH is set ([#69552](https://github.com/pytorch/pytorch/pull/69552))
    * Added support for non-contiguous inputs for `nn.functional.all_gather/reducescatter/gather` ([#75276](https://github.com/pytorch/pytorch/pull/75276))
    * Added the use of batched operations for PowerSGD ([#76041](https://github.com/pytorch/pytorch/pull/76041))
    * Changed to create UCC ProcessGroup when `ucc_lib` available ([#69564](https://github.com/pytorch/pytorch/pull/69564))
    * Changed to generalize param verification and broadcast ([#76374](https://github.com/pytorch/pytorch/pull/76374))
    * Changed to use a more reliable signaling mechanism to stop TCPStore background threads ([#76973](https://github.com/pytorch/pytorch/pull/76973))
    * Added support to disabling post-local gradient sync ([#76723](https://github.com/pytorch/pytorch/pull/76723))
    * Removed call into Python API without GIL being held in c10d ([#72928](https://github.com/pytorch/pytorch/pull/72928))
* FullyShardedDataParallel
    * Fixed `summon_full_params` when not sharded ([#72572](https://github.com/pytorch/pytorch/pull/72572))
    * Fixed 0-dim tensor optim state device ([#75243](https://github.com/pytorch/pytorch/pull/75243))
    * Fixed the synchronization of `all_gather` stream in `summon_full_params` ([#73314](https://github.com/pytorch/pytorch/pull/73314))
    * Added state_dict() save/reload in parity test ([#73366](https://github.com/pytorch/pytorch/pull/73366))
    * Changed to use `unflatten_parameter` in `_summon_full_parameters` ([#72467](https://github.com/pytorch/pytorch/pull/72467))
    * Changed to use `summon_full_params` in `get_full_params` ([#73242](https://github.com/pytorch/pytorch/pull/73242))
    * Added generic arguments for `state_dict` ([#73323](https://github.com/pytorch/pytorch/pull/73323))
    * Added generic argument forward for `load_local_state_dict` ([#73325](https://github.com/pytorch/pytorch/pull/73325))
    * Made `summon_full_params` a public method ([#73116](https://github.com/pytorch/pytorch/pull/73116))
    * Generalized `fsdp_modules()` ([#73553](https://github.com/pytorch/pytorch/pull/73553))
    * Introduced a utility API to allow users easily to set `state_dict_type` ([#73716](https://github.com/pytorch/pytorch/pull/73716))
    * Added an option to summon on rank 0 only in  `summon_full_params` ([#73903](https://github.com/pytorch/pytorch/pull/73903))
    * Enabled offload full params to CPU in `summon_full_params` ([#73904](https://github.com/pytorch/pytorch/pull/73904))
    * Removed `_lazy_init()` in rebuild full params ([#74263](https://github.com/pytorch/pytorch/pull/74263))
    * Changed to override `named_parameters()` for clean names in `summon_full_params()` ([#74333](https://github.com/pytorch/pytorch/pull/74333))
    * Changed to strip FSDP info in `summon_full_params` context, similar to `named_params` in `named_buffers` ([#74517](https://github.com/pytorch/pytorch/pull/74517))
    * Change to use param name as key in `full_optim_state_dict` ([#74879](https://github.com/pytorch/pytorch/pull/74879))
    * Enabled re-key between param names/IDs for `full_optim_state_dict` ([#74912](https://github.com/pytorch/pytorch/pull/74912))
    * Changed to register `state_dict` hooks for `FlatParamsWrapper` even if params_list is empty ([#74860](https://github.com/pytorch/pytorch/pull/74860))
    * Made `apply_to_tensors` support `OrderedDict` type ([#75560](https://github.com/pytorch/pytorch/pull/75560))
    * Added `rank0_only` to `full_optim_state_dict()` ([#75516](https://github.com/pytorch/pytorch/pull/75516))
    * Made `summon_full_params` a static method ([#75423](https://github.com/pytorch/pytorch/pull/75423))
    * Added support for PackedSequence type for `apply_for_tensors` ([#76265](https://github.com/pytorch/pytorch/pull/76265))
    * Made mixed precision API configurable ([#76423](https://github.com/pytorch/pytorch/pull/76423))
    * Validated exec order using `compute_device` ([#76664](https://github.com/pytorch/pytorch/pull/76664))
    * Improved dict inversion in `_get_param_name_to_param` to be faster([#76665](https://github.com/pytorch/pytorch/pull/76665))
    * Changed to ignore params if not in `Optim` state dict ([#76671](https://github.com/pytorch/pytorch/pull/76671))
    * Changed to include buffers in `ignored_modules` ([#76784](https://github.com/pytorch/pytorch/pull/76784))
    * Moved param/buffer name computation to constructor for `ignored_modules` ([#76994](https://github.com/pytorch/pytorch/pull/76994))
    * Changed to not clone buffers and ensure that we offload buffers to CPU if specified ([#77000](https://github.com/pytorch/pytorch/pull/77000))
    * Profiling range for `FSDP.forward` ([#76899)](https://github.com/pytorch/pytorch/pull/76899)
    * Disabled the default behavior of moving CPU module to GPU ([#77720](https://github.com/pytorch/pytorch/pull/77720))
    * Fixed `_get_param_to_unflat_param_names()` for shared params ([#75430](https://github.com/pytorch/pytorch/pull/75430))
* ShardedTensor (prototype)
    * Changed to use absolute imports for ShardMetadata instead ([#73678](https://github.com/pytorch/pytorch/pull/73678))
    * Fixed the metadata error in `init_from_local_shards` with deepcopy ([#73400](https://github.com/pytorch/pytorch/pull/73400))
    * Fixed view op and matrix ops unit test ([#77706](https://github.com/pytorch/pytorch/pull/77706))
* torch.distributed.rpc
    * Improved logging from 'unknown destination worker' ([#75811](https://github.com/pytorch/pytorch/pull/75811))
    * Improved logging for store.wait error ([#76548](https://github.com/pytorch/pytorch/pull/76548))
    * Added support for RPC Meta device ([#76882](https://github.com/pytorch/pytorch/pull/76882))
    * Changed to keep stacktrace when rewriting AttributeError ([#73720](https://github.com/pytorch/pytorch/pull/73720))
* DistributedDataParallel
    * Improved debug level and logging ([#72455](https://github.com/pytorch/pytorch/pull/72455))
    * Removed bucket replicas ([#73567](https://github.com/pytorch/pytorch/pull/73567))
    * Made `HierarchicalModelAverager` a subclass of `averagers.ModelAverager` ([#74564](https://github.com/pytorch/pytorch/pull/74564))
    * Made code simplification for `_find_process_group` function ([#75007](https://github.com/pytorch/pytorch/pull/75007))
    * Made distributed raise `ImportError` when not available ([#75975](https://github.com/pytorch/pytorch/pull/75975))
* torch.distributed.elastic
    * Created a final agent barrier to shutdown process properly ([#74931](https://github.com/pytorch/pytorch/pull/74931))

# Bug fixes

## Python API

* Fixed type promotion for `torch.where` ([#76691](https://github.com/pytorch/pytorch/pull/76691))
* Fixed `torch.clamp` to correctly propagate nans ([#77306](https://github.com/pytorch/pytorch/pull/77306))
* Fixed `torch.unique` to preserve input size when dim is zero-length ([#75764](https://github.com/pytorch/pytorch/pull/75764))
* Fixed  `torch.ravel` to also return contiguous outputs for non-contiguous inputs([#71771](https://github.com/pytorch/pytorch/pull/71771))
* Fixed `CosineAnnealingLR` to resume last learning rate on restart ([#60339](https://github.com/pytorch/pytorch/pull/60339))
* Fixed invalid shape error for `torch.fft.{irfft2,irfft2} `([#73012](https://github.com/pytorch/pytorch/pull/73012))
* Fixed `torch.set_default_dtype` to no longer crash with invalid dtype ([#72405](https://github.com/pytorch/pytorch/pull/72405))
* Fixed `torch.tril` edge case ([#75335](https://github.com/pytorch/pytorch/pull/75335))
* Fixed `torch.broadcast_shapes` to not handle shapes with negative dimensions. ([#72999](https://github.com/pytorch/pytorch/pull/72999))
* Fixed `torch.logsumexp` integral to float type promotion ([#77480](https://github.com/pytorch/pytorch/pull/77480))
* Fixed `torch.amax` and `torch.amin` for empty tensors if dim arg not provided. ([#73914](https://github.com/pytorch/pytorch/pull/73914))
* Disallowed calling `.tolist` on tensors with nullptr storage ([#75990](https://github.com/pytorch/pytorch/pull/75990))
* Fixed `.tolist` to work correctly work for 0 element tensors ([#76335](https://github.com/pytorch/pytorch/pull/76335))
* Adjusted the stubs for PyCharm autocompletion of the `Tensor` methods. ([#76712](https://github.com/pytorch/pytorch/pull/76712))
* Fixed `Optimizer.zero_grad` type annotation ([#76998](https://github.com/pytorch/pytorch/pull/76998))
* Fixed  `torch.distributions.lkj_cholesky` device error ([#73980](https://github.com/pytorch/pytorch/pull/73980))
* Fixed misplaced type annotation for `torch.distributions.transforms.CatTransform` ([#73747](https://github.com/pytorch/pytorch/pull/73747))
* Fixed `torch.clamp` scalar overloads to propagate nan ([#77371](https://github.com/pytorch/pytorch/pull/77371))
* Fixed advanced indexing assignment when  `use_deterministic_algorithms(True)` for non-contiguous tensors ([#76220](https://github.com/pytorch/pytorch/pull/76220))
* Fixed `**=` operator ([#76900](https://github.com/pytorch/pytorch/pull/76900))
* Fixed `to` to properly support permutation ([#77610](https://github.com/pytorch/pytorch/pull/77610))

## C++ API

* Used the same checks in all `grid_sampler` functions ([#75164](https://github.com/pytorch/pytorch/pull/75164))
* Fixed `mean` bug for integral tensors ([#76584](https://github.com/pytorch/pytorch/pull/76584))
* Added missing import to fix crash on loading cpp extension ([#75736](https://github.com/pytorch/pytorch/pull/75736))

## Autograd

* Fixed forward AD formula for `torch.angle` ([#77267](https://github.com/pytorch/pytorch/pull/77267))
* Fixed `torch.{minimum, maximum}` forward AD formula for float32 ([#75277](https://github.com/pytorch/pytorch/pull/75277))
* Fixed forward-mode AD formula for `torch.nn.functional.binary_cross_entropy_with_logits` ([#76322](https://github.com/pytorch/pytorch/pull/76322))
* Fixed gradients for norm related ops at zero when p < 1 to mask out nans ([#75103](https://github.com/pytorch/pytorch/pull/75103))
* Fixed forward-over-reverse for convolution to no longer fail in some cases ([#75298](https://github.com/pytorch/pytorch/pull/75298))
* Fixed `torch.autograd.gradcheck` to run with requires_grad=False when `check_forward_ad=True` ([#72309](https://github.com/pytorch/pytorch/pull/72309))
* Fixed `requires_grad`-ness to be propagated for all backends when tensors are deep-copied ([#76256](https://github.com/pytorch/pytorch/pull/76256))
* Fixed `torch.autograd.grad` to automatically needs an extra tuple when handling single outputs and `is_grads_batched=True` ([#75779](https://github.com/pytorch/pytorch/pull/75779))
* Updated forward AD metadata check to skip stride check when size is 0 ([#77269](https://github.com/pytorch/pytorch/pull/77269))
* Fixed deadlock an edge case in autograd ([#73961](https://github.com/pytorch/pytorch/pull/73961))
* Allow forking until a worker thread is created in autograd engine ([#72689](https://github.com/pytorch/pytorch/pull/72689))
* Removed some spurious warnings in the autograd engine  ([#72542](https://github.com/pytorch/pytorch/pull/72542))
* Fixed issue with `torch.utils.checkpoint.checkpoint` when both `use_reentrant` and` preserve_rng_state` set to `False` ([#76890](https://github.com/pytorch/pytorch/pull/76890))
* Fixed Python indexing set item to scalar tensor preserve autograd graph ([#78746](https://github.com/pytorch/pytorch/pull/78746))

## Build

* Added TORCH_CUDA_CU_API to CUDABlas functions ([#72340](https://github.com/pytorch/pytorch/pull/72340))
* Fixed doc build for release branches ([#72567](https://github.com/pytorch/pytorch/pull/72567))
* Moved AndroidNightly to GHA ([#74243](https://github.com/pytorch/pytorch/pull/74243))
* Changed `numModules` type to `unsigned` ([#74978](https://github.com/pytorch/pytorch/pull/74978))
* In Kineto, Changed to not search for CUPTI in default paths ([#76188](https://github.com/pytorch/pytorch/pull/76188))
* Changed to use TensorPipe libuv in Gloo ([#77312](https://github.com/pytorch/pytorch/pull/77312))

## Complex Numbers

* Fixed segmentation fault when real and imaginary attributes of a tensor are set to a number ([#73867](https://github.com/pytorch/pytorch/pull/73867))
* Fixed complex to real casting warning in the backward’s pass for Real→Complex `copy` ([#75805](https://github.com/pytorch/pytorch/pull/75805))
* Make `torch.addcmul` and `torch.addcdiv` support different complex and non-complex type args together ([#74234](https://github.com/pytorch/pytorch/pull/74234))
* Fixed `torch.isfinite` for complex to avoid overflow when real and imaginary values are finite but abs is infinite ([#76606](https://github.com/pytorch/pytorch/pull/76606)).
* Fixed complex abs/angle output format ([#77585](https://github.com/pytorch/pytorch/pull/77585))

## Dataloader

* Reset worker cycle for persistent DataLoader to ensure determinism across epochs ([#73675](https://github.com/pytorch/pytorch/pull/73675))

## LinAlg

* Fixed SVD error code handling for OpenBLAS 0.3.15+ and MKL 2022+([#72357](https://github.com/pytorch/pytorch/pull/72357))
* Fixed addmm_cpu for int64 ([#75200](https://github.com/pytorch/pytorch/pull/75200))

## Meta API

* Fixed meta kernel for `normal_` when `std` is equal to 0 ([#70085](https://github.com/pytorch/pytorch/pull/70085))
* Fixed `torch.kaiser_window` : meta for window_length > 1 ([#73733](https://github.com/pytorch/pytorch/pull/73733))
* Fixed meta kernel for `normal` ([#77740](https://github.com/pytorch/pytorch/pull/77740))

## torch.nn

* `F.pad`: Silence error when unused fill value is zero ([#76307](https://github.com/pytorch/pytorch/pull/76307))
* `nn.{Conv1d, Conv2d, Conv3d}`: Properly initialize `grad_weight` in `raw_cudnn_convolution_backward_weight_out` ([#72157](https://github.com/pytorch/pytorch/pull/72157))
* `nn.Conv2d`: Fix channels last propagation for naive algorithm ([#77347](https://github.com/pytorch/pytorch/pull/77347))
* `nn.ConvTranspose*d`: Fix to support no-batch-dim inputs with `output_size` ([#76151](https://github.com/pytorch/pytorch/pull/76151))
* `nn.CrossEntropyLoss`: Support no-batch-dim input with probability target ([#77653](https://github.com/pytorch/pytorch/pull/77653))
* `nn.CrossEntropyLoss`: Fix to avoid floating point exception for zero-size inputs ([#73837](https://github.com/pytorch/pytorch/pull/73837))
* `nn.GroupNorm`: Ensure `num_groups > 0` in `native_group_norm` ([#75270](https://github.com/pytorch/pytorch/pull/75270))
* `nn.MaxPool2d`: Properly support dilation in channels last kernel ([#76597](https://github.com/pytorch/pytorch/pull/76597))
* `nn.ParameterList`: Fix `__dir__` implementation ([#74997](https://github.com/pytorch/pytorch/pull/74997))
* `nn.{ParameterList, ParameterDict}`: Support containing any kind of object ([#70499](https://github.com/pytorch/pytorch/pull/70499))
* `nn.RReLU`: Fix to support empty tensor inputs ([#70496](https://github.com/pytorch/pytorch/pull/70496))
* `nn.utils.rnn.pad_sequence`: Fix regression; support tensor input for `sequences` ([#72436](https://github.com/pytorch/pytorch/pull/72436))
* `nn.utils.stateless.functional_call`: Properly support setting attributes during forward ([#77137](https://github.com/pytorch/pytorch/pull/77137))

## torch.fx

* Core
    * Made `map_aggregate`/`map_arg` work for NamedTuple ([#73198](https://github.com/pytorch/pytorch/pull/73198))
    * Fixed tracing for OpOverload ([#73940](https://github.com/pytorch/pytorch/pull/73940))
    * Fixed codegen for bare generic type annotations ([#74135](https://github.com/pytorch/pytorch/pull/74135))
    * Modified `__deepcopy__` to also copy _codegen ([#75851](https://github.com/pytorch/pytorch/pull/75851))
    * Fixed unnecessary recursion in `GraphModule.__call__` ([#76068](https://github.com/pytorch/pytorch/pull/76068))
    * Changed to prevent infinite recursion in GraphModule ([#73866](https://github.com/pytorch/pytorch/pull/73866))
    * Changed to preserve codegen on FX graph in transformer ([#74189](https://github.com/pytorch/pytorch/pull/74189))
* operator_schemas
    * Added back check for OpOverload ([#73978](https://github.com/pytorch/pytorch/pull/73978))
    * Fixed normalize_function to consider OpOverloads ([#76469](https://github.com/pytorch/pytorch/pull/76469))
    * Fixed for normalizing signature for op overloads ([#77182](https://github.com/pytorch/pytorch/pull/77182))
* For testing, added `super()` calls for FX TestCases ([#74216](https://github.com/pytorch/pytorch/pull/74216))
* For split_module, made split_module preserve proper placeholder names ([#74736](https://github.com/pytorch/pytorch/pull/74736))

## Sparse

* Fixed ignored beta value for sparse inputs to `torch.addmm` with non-MKL build ([#72430](https://github.com/pytorch/pytorch/pull/72430))
* Fixed float16/bf16 support for sparse inputs to `torch.addmm` ([#72559](https://github.com/pytorch/pytorch/pull/72559))
* Fixed CUDA error for `torch.mul` when given COO Tensors with zero sized dense dimensions ([#73428](https://github.com/pytorch/pytorch/pull/73428))
* Fixed incorrect results of `torch.sparse.sampled_addmm` for noncontiguous inputs ([#76590](https://github.com/pytorch/pytorch/pull/76590))
* Fixed runtime generation of doc strings for torch._masked functions by making them static instead ([#72865](https://github.com/pytorch/pytorch/pull/72865))

## CUDA

* Created jiterator cache dirs recursively ([#74592](https://github.com/pytorch/pytorch/pull/74592))
* Fixed bincount to use acc scalar for the bounds ([#76979](https://github.com/pytorch/pytorch/pull/76979))
* Avoid `collections` deprecation warning ([#72239](https://github.com/pytorch/pytorch/pull/72239))
* Disabled cuBLASLt when batch is too large. ([#73533](https://github.com/pytorch/pytorch/pull/73533))
* Abated spurious resize warnings in `MultiMarginLoss` on CUDA ([#75000](https://github.com/pytorch/pytorch/pull/75000))
* Added missing AT_CUDA_CHECK in CUDAGraph.cpp ([#74392](https://github.com/pytorch/pytorch/pull/74392))
* CUDA graphs
    * Fixed OOM inside graph capture_begin ([#76247](https://github.com/pytorch/pytorch/pull/76247))
    * Changed to allow Adam and AdamW to be capture-safe ([#77862](https://github.com/pytorch/pytorch/pull/77862))

## Intel

* Fixed Caffe2 convolution issue in AVX512 when using oneDNN v2.5.2 ([_#73290_](https://github.com/pytorch/pytorch/pull/73290))

## Composability 

* Fixed formatting of scalar tensors for the `meta` device (don't call item) ([#74376](https://github.com/pytorch/pytorch/pull/74376))
* Fixed to metadata preservation for Python tensor subclasses: preserve Python dispatch keys when copying tensor metadata ([#75644](https://github.com/pytorch/pytorch/pull/75644))
* Fixed data race on `TensorImpl::wns_pyobj_` accesses with non-GIL protected threads ([#75563](https://github.com/pytorch/pytorch/pull/75563))
* Fixed for Python garbage collector can sometimes deallocate a tensor, even when C++ still has strong references to it ([#75933](https://github.com/pytorch/pytorch/pull/75933))
* Added better error checking to `TensorImpl::size_between_dim_`. ([#76719](https://github.com/pytorch/pytorch/pull/76719))
* Changed to ensure that `torch.memory_format` instances are singletons ([#77543](https://github.com/pytorch/pytorch/pull/77543))

## Profiler

* Avoided picking up old CUPTI headers ([#72761](https://github.com/pytorch/pytorch/pull/72761))
* Kineto submodule update and fixes ([#75206](https://github.com/pytorch/pytorch/pull/75206))
* Fixed segfault in AppendOnlyList ([#78084](https://github.com/pytorch/pytorch/pull/78084))

## Vulkan

* Fixed a bug in the Vulkan implementation of `aten::tanh` where inputs of large magnitudes would result in numerically unstable results ([#73107](https://github.com/pytorch/pytorch/pull/73107))
* Fixed a bug in the Vulkan implementation of `aten::add`, `aten::sub`, `aten::mul`, and `aten::div` where passing in a single element tensor as a second argument would result in an assertion error ([#73108](https://github.com/pytorch/pytorch/pull/73108))

## Mobile

* Changed to protect against threading errors when tracing models with parallel operators ([#73327](https://github.com/pytorch/pytorch/pull/73327))
* Changed to ensure error messages are preserved from Metal and CoreML Backend ([#77430](https://github.com/pytorch/pytorch/pull/77430), [#76236](https://github.com/pytorch/pytorch/pull/76263))
* Changed to ensure the iOS test app is working correctly ([#74090](https://github.com/pytorch/pytorch/pull/74090))
* Fixed off-by-one error in tupleIndex ([#72447](https://github.com/pytorch/pytorch/pull/72447))
* Fixed error in export of models containing nested NamedTuple ([#75996](https://github.com/pytorch/pytorch/pull/75996))

## Distributed

* torch.distributed
    * Fixed process group wrapper check for Gloo ([#72657](https://github.com/pytorch/pytorch/pull/72657) (https://github.com/pytorch/pytorch/pull/72657))
    * Changes to catch CUDA library runtime error (driver shutting down) during the exit of ProcessGroup ([#74258](https://github.com/pytorch/pytorch/pull/74258) (https://github.com/pytorch/pytorch/pull/74258))
    * Fixed NCCL version string ([#73333](https://github.com/pytorch/pytorch/pull/73333) (https://github.com/pytorch/pytorch/pull/73333))
    * Add retry DNS lookup failures ([#74641](https://github.com/pytorch/pytorch/pull/74641) (https://github.com/pytorch/pytorch/pull/74641))
    * Validated that tensors are contiguous in ProcessGroupNCCL ([#77809](https://github.com/pytorch/pytorch/pull/77809) (https://github.com/pytorch/pytorch/pull/77809))
    * Fixed sign-compare in c10d/Utils.hpp ([#75081](https://github.com/pytorch/pytorch/pull/75081) (https://github.com/pytorch/pytorch/pull/75081))
    * Fixed NCCL gather outputs on non-root ranks ([#75535](https://github.com/pytorch/pytorch/pull/75535) (https://github.com/pytorch/pytorch/pull/75535))
    * Fixed batch_isend_irecv ([#74701](https://github.com/pytorch/pytorch/pull/74701) (https://github.com/pytorch/pytorch/pull/74701))
    * Disabled RPC profiling for kineto profilers ([#76234](https://github.com/pytorch/pytorch/pull/76234) (https://github.com/pytorch/pytorch/pull/76234))
    * Typo fix in generated module name ([#76880](https://github.com/pytorch/pytorch/pull/76880) (https://github.com/pytorch/pytorch/pull/76880))
    * Fixed broadcast for channels-last tensors ([#79071](https://github.com/pytorch/pytorch/pull/79071) (https://github.com/pytorch/pytorch/pull/79071))
* DistributedDataParallel
    * Disabled bucketing for the first iteration ([#72843](https://github.com/pytorch/pytorch/pull/72843) (https://github.com/pytorch/pytorch/pull/72843))
    * Fixed SyncBatchNorm for empty inputs ([#74944](https://github.com/pytorch/pytorch/pull/74944) (https://github.com/pytorch/pytorch/pull/74944))
    * Added a guard for non CPU/CUDA devices ([#75247](https://github.com/pytorch/pytorch/pull/75247) (https://github.com/pytorch/pytorch/pull/75247))
    * Fixed bug where *getstate* of DDP looks for self._replicated_tensor_module when not using ReplicatedTensor. ([#76349](https://github.com/pytorch/pytorch/pull/76349) (https://github.com/pytorch/pytorch/pull/76349))
    * Fixed post_localSGD_optimizer by calling optim.step only once when there are multiple param groups or params ([#74737](https://github.com/pytorch/pytorch/pull/74737) (https://github.com/pytorch/pytorch/pull/74737))
    * Fixed PostLocalSGDOptimizer and ModelAverager average ([#74894](https://github.com/pytorch/pytorch/pull/74894) (https://github.com/pytorch/pytorch/pull/74894))
* ShardedTensor (prototype)
    * Fixed Sharding spec inference to avoid invalid chunk sharding to be inferred as chunkshardingspec ([#75296](https://github.com/pytorch/pytorch/pull/75296) (https://github.com/pytorch/pytorch/pull/75296))
* FullyShardedDataParallel
    * Fixed no_sync() + FULL_SHARD root all-gather behavior ([#75901](https://github.com/pytorch/pytorch/pull/75901) (https://github.com/pytorch/pytorch/pull/75901))
    * Fixed exec order validation (static variable issue) ([#76273](https://github.com/pytorch/pytorch/pull/76273) (https://github.com/pytorch/pytorch/pull/76273))
    * Fixed local_state_dict and state_dict_type bugs ([#77101](https://github.com/pytorch/pytorch/pull/77101) (https://github.com/pytorch/pytorch/pull/77101))
    * Fixed FSDP wrapping for batchnorm when mixed precision enabled ([#77234](https://github.com/pytorch/pytorch/pull/77234) (https://github.com/pytorch/pytorch/pull/77234))
    * Fixed CheckpointWrapper state_dict to enable wrapped modules loaded into non-checkpointed wrapped module ([#77224](https://github.com/pytorch/pytorch/pull/77224) (https://github.com/pytorch/pytorch/pull/77224))
    * Changed to relax exec order valid. to only forward pass ([#76556](https://github.com/pytorch/pytorch/pull/76556) (https://github.com/pytorch/pytorch/pull/76556))
    * Changed to not check forward order in eval mode ([#77195](https://github.com/pytorch/pytorch/pull/77195) (https://github.com/pytorch/pytorch/pull/77195))
    * Changed to pass device_id into recursive_wrap for FSDP ([#77491](https://github.com/pytorch/pytorch/pull/77491) (https://github.com/pytorch/pytorch/pull/77491))

## JIT/TorchScript

* torch.jit.fuser("fuser1") is supposed to enable NNC fusion, but it currently only enables gpu fusion. This will enable CPU fusion as well. ([#74078](https://github.com/pytorch/pytorch/pull/74078))
* Fixed bug where when parsing a Python TernaryIf expression (`x if y else z`)  was not being parsed into TorchScript using `torch.jit.script` as right associative ([#68416](https://github.com/pytorch/pytorch/pull/68416))
* Got rid of TorchScript sparse tensor is experimental warning. ([#73874](https://github.com/pytorch/pytorch/pull/73874))
* Custom post-processing passes registered through `torch::jit::RegisterPass` now have access to profiled Tensor Type Specializations ([#71748](https://github.com/pytorch/pytorch/pull/71748))
* When registering a custom print handler for `prim::print()` inside `torch.deploy`, we restore the default print handler when all Python environments are destroyed to prevent errors from not having a Python environment. ([#74513](https://github.com/pytorch/pytorch/pull/74513))
* When running `torch.jit.freeze` on the backward passes of conv (`conv_bn`) with reduced precision (eg `bfloat16`) , fusions will respect the precision of the original op, instead of promoting to `float32`  ([#77042](https://github.com/pytorch/pytorch/pull/77042))
* Loosened `torch.jit.script` type checks that were too strict for the `torch.nn.LPPool2D` and `torch.nn.functional.lp_pool2d` functions ([#73287](https://github.com/pytorch/pytorch/pull/73287))
* `torch.nn.ParameterList` is now subscriptable in TorchScript  ([#75479](https://github.com/pytorch/pytorch/pull/75479))

## Quantization

* Fixed `get_module_type` for fusion ([#72735](https://github.com/pytorch/pytorch/pull/72735))
* Fixed bug in QuantWrapper with DeQuant qconfig ([#73671](https://github.com/pytorch/pytorch/pull/73671))
* Fixed observer insertion through dtype propagation ([#73274](https://github.com/pytorch/pytorch/pull/73274))
* Only do reference module swapping for floating point fused modules ([#74231](https://github.com/pytorch/pytorch/pull/74231))
* Fixed dynamic weighted op lowering when input is used multiple times ([#74364](https://github.com/pytorch/pytorch/pull/74364))
* Fixed `get_default_qconfig_dict` for fused modules ([#75838](https://github.com/pytorch/pytorch/pull/75838))
* Fixed bug for ave pooling in FX quant ([#73054](https://github.com/pytorch/pytorch/pull/73054))
* Fixed FX QAT for untraceable modules ([#74277](https://github.com/pytorch/pytorch/pull/74277))
* Fixed `qmin`/`qmax` when using customized ‘qrange’ ([#74717](https://github.com/pytorch/pytorch/pull/74717))

## ONNX

* Fixed repeat interleave when repeats and dim is 1 ([#73760](https://github.com/pytorch/pytorch/pull/73760))
* Fixed ONNX gather shape inference ([#73607](https://github.com/pytorch/pytorch/pull/73607))
* Fixed 1d case flatten export ([#74595](https://github.com/pytorch/pytorch/pull/74595))
* Fixed opset_version checked before set ([#76928](https://github.com/pytorch/pytorch/pull/76928))
* Fixed an assertion failure involving Slice ([#72989](https://github.com/pytorch/pytorch/pull/72989))
* Fixed LSTM reshape shape inference regression ([#72532](https://github.com/pytorch/pytorch/pull/72532))
* Fixed Caffe2 ONNX export for environment with newer ONNX ([#75718)](https://github.com/pytorch/pytorch/pull/75718/)
* Refactored test/onnx/test_onnx_export.py for better code reuse ([#76851](https://github.com/pytorch/pytorch/pull/76851))
* Fixed `aten::to("cpu")` and `aten::to(device="cpu")` ([#76498](https://github.com/pytorch/pytorch/pull/76498))
* Fixed BatchNormalization for invalid dtype ([#74875](https://github.com/pytorch/pytorch/pull/74875))
* Added Autocast support for `einsum` ([#71916](https://github.com/pytorch/pytorch/pull/71916))

## torch.package

* Deploy: added dummy metadata for builtin packages ([#76211](https://github.com/pytorch/pytorch/pull/76211))
* Enabled module modification during repackaging ([#71520](https://github.com/pytorch/pytorch/pull/71520))
* Added test case for repackaging parent module ([#72367](https://github.com/pytorch/pytorch/pull/72367))
* Fixed orderedimporter dummy package check ([#72533](https://github.com/pytorch/pytorch/pull/72533))
* Improved error message for module detection on saving pass ([#73106](https://github.com/pytorch/pytorch/pull/73106))
* Changed to allow torch/csrc/deploy/interpreter/Optional.hpp to be allowed into the wheel distribution ([#74643](https://github.com/pytorch/pytorch/pull/74643))

# Performance

## Python API

* Improved `torch.topk` performance on CUDA ([#74267](https://github.com/pytorch/pytorch/pull/74267))
* Added SIMD horizontal reduce to improve `torch.log_softmax` and `torch.softmax` performance on CPU ([#73953](https://github.com/pytorch/pytorch/pull/73953))
* Made small optimizations for `torch.view` ([#72626](https://github.com/pytorch/pytorch/pull/72626))
* Optimized dim reduce performance on `torch.{norm,` `argmax, argmin}` ([#72083](https://github.com/pytorch/pytorch/pull/72083))
* Improved CPU performance for `torch.log_softmax` when dim != -1 on both float32 and bfloat16 ([#72163](https://github.com/pytorch/pytorch/pull/72163))
* Improved `torch.softmax` `dim=-1` performance on bfloat16 by adding more fusion ([#76278](https://github.com/pytorch/pytorch/pull/76278))
* Removed duplicate call to objective function in strong Wolfe line search in `L-BFGS` optimizer. ([#72773](https://github.com/pytorch/pytorch/pull/72773))

## Autograd

* Optimized code-generated in-place forward AD formulas ([#74017](https://github.com/pytorch/pytorch/pull/74017))
* Added a fast path for `torch.{stack, cat}` forward AD computation when tangents are zero-filled ([#75590](https://github.com/pytorch/pytorch/pull/75590))
* Reduced forward AD recomputation for `linalg.{eig,eigh,svd}` when function returns multiple outputs ([#75583](https://github.com/pytorch/pytorch/pull/75583))

## Sparse

* Improved performance of `index_select` for COO inputs on CPU ([#72710](https://github.com/pytorch/pytorch/pull/72710))
* Improved performance of `index_add` on CUDA ([#76996](https://github.com/pytorch/pytorch/pull/76996))

## Dataloader

* Improved the performance of `BatchSampler` ([#76951](https://github.com/pytorch/pytorch/pull/76951))

## AMD

* Enabled foreach fast path ([#74417](https://github.com/pytorch/pytorch/pull/74417))
* Reverted cat operator performance work-around ([#74129](https://github.com/pytorch/pytorch/pull/74129))

## CUDA

* Removed sync in embedding ([#70943](https://github.com/pytorch/pytorch/pull/70943))
* Added fused addmm path in linear for contiguous 3D input ([#72728](https://github.com/pytorch/pytorch/pull/72728))
* Changed to use cub 1.15's latest scan-by-key algorithm to replace thrust for `Embedding.cu` and `EmbeddingBag.cu` ([#66580](https://github.com/pytorch/pytorch/pull/66580))
* Changed to use `cub::DeviceSelect::UniqueByKey` for EmbeddingBackward ([#68376](https://github.com/pytorch/pytorch/pull/68376))
* Changed to use cuBLASLt interface for bias fusion ([#72148](https://github.com/pytorch/pytorch/pull/72148))
* Set workspace size for cuBLASLt interface 1M ([#73439](https://github.com/pytorch/pytorch/pull/73439))
* Added fastAtomicAdd to scatter_add [v2] ([#75545](https://github.com/pytorch/pytorch/pull/75545))
* Added a new optimized cuDNN RNN algorithm for small RNN hidden_size ([#73211](https://github.com/pytorch/pytorch/pull/73211))
* Avoided CPU Sync in SyncBatchNorm When Capturing CUDA Graphs ([#78810](https://github.com/pytorch/pytorch/pull/78810)) ([_commit_](https://github.com/pytorch/pytorch/commit/2652da29ab6c0d690bfb543bee958f50c0b86451))
* Added Autocast CPU doc ([#68567](https://github.com/pytorch/pytorch/pull/68567))
* Documented CUDA 11.5 windows issue ([#73013](https://github.com/pytorch/pytorch/pull/73013))
* Added `__all__` for `torch.cuda.memory` ([#76490](https://github.com/pytorch/pytorch/pull/76490))

## Composability 

* Improved performance for forward-mode AD with `at::sub`: added ZeroTensor fast-path ([#75587](https://github.com/pytorch/pytorch/pull/75587))

## torch.nn

* `nn.EmbeddingBag`: Removed out-of-bounds check to improve CUDA performance ([#74767](https://github.com/pytorch/pytorch/pull/74767))
* `nn.GELU`: Added support tanh-based approximation ([#61439](https://github.com/pytorch/pytorch/pull/61439))
* `nn.GroupNorm`: Improved channels last performance on CPU ([#69067](https://github.com/pytorch/pytorch/pull/69067))
* `nn.LayerNorm`: Improved bfloat16 performance on CPU ([#71376](https://github.com/pytorch/pytorch/pull/71376))
* `nn.LayerNorm`: Added mixed data type mode for forward path ([#73844](https://github.com/pytorch/pytorch/pull/73844))
* `nn.MultiheadAttention`: Fast path using nested tensors for inference under specific conditions ([#77924](https://github.com/pytorch/pytorch/pull/77924), [#77761](https://github.com/pytorch/pytorch/pull/77761))
* `nn.MultiheadAttention`: Fuse the `attn_mask` addition ([#73219](https://github.com/pytorch/pytorch/pull/73219), [#72871](https://github.com/pytorch/pytorch/pull/72871)))
* `nn.MultiheadAttention`: Native fast path under specific conditions ([#75809](https://github.com/pytorch/pytorch/pull/75809), [#76333](https://github.com/pytorch/pytorch/pull/76333), [#72944](https://github.com/pytorch/pytorch/pull/72944), [#72941](https://github.com/pytorch/pytorch/pull/72941), [#72671](https://github.com/pytorch/pytorch/pull/72671), [#72375](https://github.com/pytorch/pytorch/pull/72375), [#72458](https://github.com/pytorch/pytorch/pull/72458), [#72464](https://github.com/pytorch/pytorch/pull/72464), [#72463](https://github.com/pytorch/pytorch/pull/72463))
* `nn.MultiheadAttention`: Preserve identity relationships among query, key, and value for `batch_first=True` ([#73053](https://github.com/pytorch/pytorch/pull/73053))
* `nn.utils.weight_norm`: Added native CPU kernel ([#73845](https://github.com/pytorch/pytorch/pull/73845))
* `F.grid_sample`: Improved backward pass scaling with input size for 3d implementation ([#71759](https://github.com/pytorch/pytorch/pull/71759))

## Benchmark

* Added binary to benchmark model load speed ([#74700](https://github.com/pytorch/pytorch/pull/74700))

## Profiler

* Optimized Profiler overhead and improve scalability ([#71538](https://github.com/pytorch/pytorch/pull/71538), [#73409](https://github.com/pytorch/pytorch/pull/73409), [#73855](https://github.com/pytorch/pytorch/pull/73855), [#74151](https://github.com/pytorch/pytorch/pull/74151), [#74241](https://github.com/pytorch/pytorch/pull/74241), [#74484](https://github.com/pytorch/pytorch/pull/74484), [#74888](https://github.com/pytorch/pytorch/pull/74888))
* Optimized RecordFunction machinery ([#75807](https://github.com/pytorch/pytorch/pull/75807), [#76017](https://github.com/pytorch/pytorch/pull/76017), [#76016](https://github.com/pytorch/pytorch/pull/76016))

## Mobile

* Reduced unnecessary reference count bumps while parsing ByteCode. ([#72523](https://github.com/pytorch/pytorch/pull/72523))

## Quantization

* Improved multi-core performance of `qavg_pool2d` ([#69517](https://github.com/pytorch/pytorch/pull/69517))
* Improved multi-core performance of `qmax_pool2d` ([#69598](https://github.com/pytorch/pytorch/pull/69598))
* Improved multi-core performance of `qbatch_norm2d` ([#69599](https://github.com/pytorch/pytorch/pull/69599))
* Improved multi-core performance of `qupsample_nearest2d` ([#69600](https://github.com/pytorch/pytorch/pull/69600))
* Improved multi-core performance of `qupsample_bilinear2d` ([#69601](https://github.com/pytorch/pytorch/pull/69601))
* Improved `qcat_nhwc` performance on both multi-core and single-core ([#69667](https://github.com/pytorch/pytorch/pull/69667))
* Added Optimized QInt8 Quantize Tensor Arm ([#76245](https://github.com/pytorch/pytorch/pull/76245))

# Documentation

## Python API

* Updated `torch.amp` document with CPU Training/Inference Examples ([#77244](https://github.com/pytorch/pytorch/pull/77244))
* Updated `torch.utils.dlpack.from_dlpack` documentation ([#70543](https://github.com/pytorch/pytorch/pull/70543))
* Fixed indexing of class names in docs for `torch.{device,` `dtype, layout, memory_format}` ([#73632](https://github.com/pytorch/pytorch/pull/73632))
* Fixed `torch.asarray` docs and add test case ([#73736](https://github.com/pytorch/pytorch/pull/73736))
* Removed misleading statement in `optim.Optimizer` docs ([#76967](https://github.com/pytorch/pytorch/pull/76967))
* Fixed nesterov momentum equation for `torch.optim.SGD` ([#76639](https://github.com/pytorch/pytorch/pull/76639))
* Added missing zero-ing step in `torch.optim.Rprop` algorithm ([#75555](https://github.com/pytorch/pytorch/pull/75555))
* Fixed docs about type promotion of `torch.`{`bitwise_left_shift,bitwise_right_shift}` ([#77613](https://github.com/pytorch/pytorch/pull/77613))
* Fixed docstring for `torch.roll` ([#74880](https://github.com/pytorch/pytorch/pull/74880))
* Added docs for `torch.scatter_reduce` ([#73125](https://github.com/pytorch/pytorch/pull/73125))
* Automatically generate docstring for `torch.distributions.kl_divergence` ([#72845](https://github.com/pytorch/pytorch/pull/72845))
* Miscellaneous documentation improvements ([#74796](https://github.com/pytorch/pytorch/pull/74796), [#76369](https://github.com/pytorch/pytorch/pull/76369))

## C++ API

* Exposed documentation for `unfold` ([#74224](https://github.com/pytorch/pytorch/pull/74224))

## Autograd

* Fixed error in “Autograd Mechanics” doc’s eval mode section ([#74807](https://github.com/pytorch/pytorch/pull/74807))
* Added “Gradients for non-differentiable functions” section in "Autograd Mechanics" doc to explain how gradients are chosen in edge cases ([#76898](https://github.com/pytorch/pytorch/pull/76898))
* Added  link to "Custom function double backward tutorial" from "Extending Pytorch" page ([#72584](https://github.com/pytorch/pytorch/pull/72584))
* Documented forward AD interaction with grad mode ([#72216](https://github.com/pytorch/pytorch/pull/72216))
* Fixed code examples to run successfully ([#74044](https://github.com/pytorch/pytorch/pull/74044))

## Dataloader

* Updated DataLoader docstring about `prefetch_factor` to reflect right amount of batches prefetched by `DataLoader` ([#74558](https://github.com/pytorch/pytorch/pull/74558))
* Fixed docstring for `collate_fn` ([#76594](https://github.com/pytorch/pytorch/pull/76594))

## LinAlg

* Extrapolated on equiv between linalg @ and solve ([#71769](https://github.com/pytorch/pytorch/pull/71769))
* Updated `torch.lu_unpack` docs ([#73803](https://github.com/pytorch/pytorch/pull/73803))

## torch.nn

* `nn.CosineEmbeddingLoss`: Use correct cosine similarity term instead of cosine distance ([#75188](https://github.com/pytorch/pytorch/pull/75188))
* `nn.Hardtanh`: Use `min_val` and `max_val` in function definition ([#75789](https://github.com/pytorch/pytorch/pull/75789))
* `nn.KLDivLoss`: Fixed `log_target` example ([#74945](https://github.com/pytorch/pytorch/pull/74945))
* `nn.``LazyModuleMixin` Fixed typo in docs ([#76269](https://github.com/pytorch/pytorch/pull/76269))
* `nn.LSTM`: Clarified docs for outputs vs. hidden states ([#74291](https://github.com/pytorch/pytorch/pull/74291))
* `nn.Module`: Fixed docs by moving `_version` class variable after docstring ([#72912](https://github.com/pytorch/pytorch/pull/72912))
* `nn.Module`: Fixed docstring typo for `get_submodule()` ([#73018](https://github.com/pytorch/pytorch/pull/73018))
* `nn.Module`: Fixed URL for creating GitHub issues ([#73411](https://github.com/pytorch/pytorch/pull/73411))
* `nn.RNN`: Fixed math notation for linear projections ([#77082](https://github.com/pytorch/pytorch/pull/77082))
* `nn.Transformer`: Detailed 3D tensor shape for masks ([#75552](https://github.com/pytorch/pytorch/pull/75552))
* `nn.TripletMarginLoss`: Fixed formatting error ([#76629](https://github.com/pytorch/pytorch/pull/76629))
* `F.{conv3d, conv_transpose3d, fold, linear}, nn.{AdaptiveAvgPool3d, AvgPool1d, MultiMarginLoss, PairwiseDistance, TripletMarginLoss}`: Fixed doc formatting regressions ([#73014](https://github.com/pytorch/pytorch/pull/73014))
* `F.multi_head_attention_forward`: Added to functional rst ([#72675](https://github.com/pytorch/pytorch/pull/72675))
* `F.multi_head_attention_forward`: Fixed math formatting, misc edit ([#74181](https://github.com/pytorch/pytorch/pull/74181))
* `F.pad`: Fixed supported input shapes in docs ([#76117](https://github.com/pytorch/pytorch/pull/76117))
* `nn.init.trunc_normal_`: Added to `nn.init` docs ([#76896](https://github.com/pytorch/pytorch/pull/76896))
* `nn.utils.clip_grad_norm_`: Fixed return value description ([#76230](https://github.com/pytorch/pytorch/pull/76230))
* `nn.Convolution`: Added note on complex support ([#](https://github.com/pytorch/pytorch/pull/78351)[78351](https://github.com/pytorch/pytorch/pull/78351))

## torch.fx

* Added better error message for FX when using concrete_args ([#76600](https://github.com/pytorch/pytorch/pull/76600))

## Composability

* Added docs for Python Registration ([#79481](https://github.com/pytorch/pytorch/pull/79481))

## Sparse

* Added missing entry for `torch.sparse.sampled_addmm` on website ([#72312](https://github.com/pytorch/pytorch/pull/72312))

## Mobile

* Documentation improvement in test_backend_with_compiler (52c516ecb8)
* Added README for mobile model test ([#76385](https://github.com/pytorch/pytorch/pull/76385), [#76409](https://github.com/pytorch/pytorch/pull/76409))

## Distributed

* torch.distributed
    * Clarified the input of PostLocalSGDState ([#72792](https://github.com/pytorch/pytorch/pull/72792))
    * Added a reference to hierarchical SGD for Model Averaging ([#73823](https://github.com/pytorch/pytorch/pull/73823))
    * Updated documentation about NCCL environment variables ([#74006](https://github.com/pytorch/pytorch/pull/74006))
    * Added `TORCH_CPP_LOG_LEVEL` to the docs ([#76625](https://github.com/pytorch/pytorch/pull/76625))
* FullyShardedDataParallel
    * Improved the documentation of state_dict ([#73453](https://github.com/pytorch/pytorch/pull/73453))
    * Updated `full_optim_state_dict` warning ([#75109](https://github.com/pytorch/pytorch/pull/75109))
    * Added warning when fail to clone ([#74946](https://github.com/pytorch/pytorch/pull/74946))
    * Added mixed precision doc ([#76130](https://github.com/pytorch/pytorch/pull/76130))
    * Added warnings for shared params and updated doc ([#77726](https://github.com/pytorch/pytorch/pull/77726))
    * Fixed `state_dict_type()` example ([#77848](https://github.com/pytorch/pytorch/pull/77848))
    * Reworded device placement warning ([#77850](https://github.com/pytorch/pytorch/pull/77850))
    * Updated `state_dict()` docstring ([#77853](https://github.com/pytorch/pytorch/pull/77853))
* torch.distributed.rpc
    * Added note in RPC docs about retries. ([#73601](https://github.com/pytorch/pytorch/pull/73601))
* DistributedDataParallel
    * Updated the comment for Forward and Backward Hook ([#74063](https://github.com/pytorch/pytorch/pull/74063))
    * Added documentation for c10d log levels ([#73361](https://github.com/pytorch/pytorch/pull/73361))
* torch.distributed.elastic
    * Added documentation clarifying that `torchrun` is a console script to `torch.distributed.run` ([#73598](https://github.com/pytorch/pytorch/pull/73598))

## TorchScript

* Corrected torch.jit.Attribute docs to say that it needs to be used in subclasses of torch.jit.ScriptModule, not torch.nn.Module ([#74653](https://github.com/pytorch/pytorch/pull/74653))

## Quantization

* Added docs for `torch.quantize_per_tensor_dynamic` ([#72311](https://github.com/pytorch/pytorch/pull/72311))
* Fixed typo in quantization docs ([#73511](https://github.com/pytorch/pytorch/pull/73511))
* Grammatically updated quantization tech doc ([#74436](https://github.com/pytorch/pytorch/pull/74436))
* Added best practices for quantization accuracy debugging ([#77536](https://github.com/pytorch/pytorch/pull/77536))
* Improved rendered documentation for backend_config_dict ([#77535](https://github.com/pytorch/pytorch/pull/77535))
* Autogenerated quantization backend configs for documentation ([#75126](https://github.com/pytorch/pytorch/pull/75126))
* Added more docs for quantization.rst ([#75998](https://github.com/pytorch/pytorch/pull/75998))
* Fixed formatting for quantization.rst ([#76223](https://github.com/pytorch/pytorch/pull/76223))

## ONNX

* Added the developing PyTorch ONNX exporter wiki doc link ([_#72663_](https://github.com/pytorch/pytorch/pull/72663))
* Added list of supported ATen ops to [_torch.onnx_](https://pytorch.org/docs/master/onnx.html#list-of-supported-operators) page ([_#74397_](https://github.com/pytorch/pytorch/pull/74397))

## Visualization

* `torch.utils.tensorboard.writer:` Added missing 'dataformats' argument to 'add_image' docs. ([#48834](https://github.com/pytorch/pytorch/pull/48834))
# ===== RELEASE pytorch/pytorch v1.13.0 =====

# Pytorch 1.13 Release Notes

* Highlights
* Backwards Incompatible Changes
* New Features
* Improvements
* Performance
* Documentation
* Developers

# Highlights

We are excited to announce the release of PyTorch 1.13! This includes stable versions of BetterTransformer. We deprecated CUDA 10.2 and 11.3 and completed migration of CUDA 11.6 and 11.7. Beta includes improved support for Apple M1 chips and functorch, a library that offers composable vmap (vectorization) and autodiff transforms, being included in-tree with the PyTorch release. This release is composed of over 3,749 commits and 467 contributors since 1.12.1. We want to sincerely thank our dedicated community for your contributions.

Summary:

* The BetterTransformer feature set supports fastpath execution for common Transformer models during Inference out-of-the-box, without the need to modify the model. Additional improvements include accelerated add+matmul linear algebra kernels for sizes commonly used in Transformer models and Nested Tensors is now enabled by default.

* Timely deprecating older CUDA versions allows us to proceed with introducing the latest CUDA version as they are introduced by Nvidia®, and hence allows support for C++17 in PyTorch and new NVIDIA Open GPU Kernel Modules.

* Previously, functorch was released out-of-tree in a separate package. After installing PyTorch, a user will be able to `import functorch` and use functorch without needing to install another package.

* PyTorch is offering native builds for Apple® silicon machines that use Apple's new M1 chip as a beta feature, providing improved support across PyTorch's APIs.

|Stable	|Beta	|Prototype	|
|---	|---	|---	|
|<ul><li>Better Transformer</li><li>CUDA 10.2 and 11.3 CI/CD Deprecation </li></ul> | <ul><li>Enable Intel® VTune™ Profiler's Instrumentation and Tracing Technology APIs</li><li>Extend NNC to support channels last and bf16</li><li>Functorch now in PyTorch Core Library</li><li>Beta Support for M1 devices</li></ul>	| <ul><li>Arm® Compute Library backend support for AWS Graviton</li><li> CUDA Sanitizer</li></ul> |

You can check the blogpost that shows the new features [here](https://pytorch.org/blog/PyTorch-1.13-release/).

# Backwards Incompatible changes

## Python API

### **uint8 and all integer dtype masks are no longer allowed in Transformer** **(#87106)**

Prior to 1.13, `key_padding_mask` could be set to uint8 or other integer dtypes in `TransformerEncoder` and `MultiheadAttention`, which might generate unexpected results. In this release, these dtypes are not allowed for the mask anymore. Please convert them to `torch.bool` before using.

1.12.1

```python
>>> layer = nn.TransformerEncoderLayer(2, 4, 2)
>>> encoder = nn.TransformerEncoder(layer, 2)
>>> pad_mask = torch.tensor([[1, 1, 0, 0]], dtype=torch.uint8)
>>> inputs = torch.cat([torch.randn(1, 2, 2), torch.zeros(1, 2, 2)], dim=1)
# works before 1.13
>>> outputs = encoder(inputs, src_key_padding_mask=pad_mask)
```

1.13

```python
>>> layer = nn.TransformerEncoderLayer(2, 4, 2)
>>> encoder = nn.TransformerEncoder(layer, 2)
>>> pad_mask = torch.tensor([[1, 1, 0, 0]], dtype=torch.bool)
>>> inputs = torch.cat([torch.randn(1, 2, 2), torch.zeros(1, 2, 2)], dim=1)
>>> outputs = encoder(inputs, src_key_padding_mask=pad_mask)
```

### **Updated `torch.floor_divide` to perform floor division** **(#78411)**

Prior to 1.13, `torch.floor_divide` erroneously performed truncation division (i.e. truncated the quotients). In this release, it has been fixed to perform floor division. To replicate the old behavior, use `torch.div` with `rounding_mode='trunc'`.

1.12.1

```python
>>> a = torch.tensor([4.0, -3.0])
>>> b = torch.tensor([2.0, 2.0])
>>> torch.floor_divide(a, b)
tensor([ 2., -1.])
```

1.13

```python
>>> a = torch.tensor([4.0, -3.0])
>>> b = torch.tensor([2.0, 2.0])
>>> torch.floor_divide(a, b)
tensor([ 2., -2.])
# Old behavior can be replicated using torch.div with rounding_mode='trunc'
>>> torch.div(a, b, rounding_mode='trunc')
tensor([ 2., -1.])
```

### **Fixed `torch.index_select` on CPU to error that index is out of bounds when the `source` tensor is empty (#77881)**

Prior to 1.13, `torch.index_select` would return an appropriately sized tensor filled with random values on CPU if the source tensor was empty. In this release, we have fixed this bug so that it errors out. A consequence of this is that `torch.nn.Embedding` which utilizes `index_select` will error out rather than returning an empty tensor when `embedding_dim=0` and `input` contains indices which are out of bounds. The old behavior cannot be reproduced with `torch.nn.Embedding`, however since an Embedding layer with `embedding_dim=0` is a corner case this behavior is unlikely to be relied upon.

1.12.1

```python
>>> t = torch.tensor([4], dtype=torch.long)
>>> embedding = torch.nn.Embedding(3, 0)
>>> embedding(t)
tensor([], size=(1, 0), grad_fn=<EmbeddingBackward0>)
```

1.13

```python
>>> t = torch.tensor([4], dtype=torch.long)
>>> embedding = torch.nn.Embedding(3, 0)
>>> embedding(t)
RuntimeError: INDICES element is out of DATA bounds, id=4 axis_dim=3
```

### Disallow overflows when tensors are constructed from scalars (#82329)

Prior to this PR, overflows during tensor construction from scalars would not throw an error. In 1.13, such cases will error.

1.12.1

```python
>>> torch.tensor(1000, dtype=torch.int8)
tensor(-24, dtype=torch.int8)
```

1.13

```python
>>> torch.tensor(1000, dtype=torch.int8)
RuntimeError: value cannnot be converted to type int8 without overflow
```

### **Error on indexing a cpu tensor with non-cpu indices (#69607)**

Prior to 1.13, `cpu_tensor[cuda_indices]` was a valid program that would return a cpu tensor. The original use case for mixed device indexing was for `non_cpu_tensor[cpu_indices]`, and allowing the opposite was unintentional (`cpu_tensor[non_cpu_indices]`). This behavior appears to be rarely used, and a refactor of our indexing kernels made it difficult to represent an op that takes in (cpu_tensor, non_cpu_tensor) and returns another cpu_tensor, so it is now an error.

To replicate the old behavior for `base[indices]`, you can ensure that either `indices` lives on the CPU device, or `base` and `indices` both live on the same device.

1.12.1

```python
>>> a = torch.tensor([1.0, 2.0, 3.0])
>>> b = torch.tensor([0, 2], device='cuda')
>>> a[b]
tensor([1., 3.])
```

1.13

```python
>>> a = torch.tensor([1.0, 2.0, 3.0])
>>> b = torch.tensor([0, 2], device='cuda')
>>> a[b]
RuntimeError: indices should be either on cpu or on the same device as the indexed tensor (cpu)
# Old behavior can be replicated by moving b to CPU, or a to CUDA
>>> a[b.cpu()]
tensor([1., 3.])
>>> a.cuda()[b]
tensor([1., 3.], device='cuda:0')
```


### Remove deprecated `torch.eig`,` torch.matrix_rank`, `torch.lstsq` (#70982, #70981, #70980)
The deprecation cycle for the above functions has been completed and they have been removed in the 1.13 release.

## torch.nn

### Enforce that the `bias` has the same dtype as `input` and `weight` for convolutions on CPU (#83686)

To align with the implementation on other devices, the CPU implementation for convolutions was updated to enforce that the `dtype` of the `bias` matches the `dtype` of the `input` and `weight`.

1.12.1

```python
# input and weight are dtype torch.int64
# bias is torch.float32
>>> out = torch.nn.functional.conv2d(input, weight, bias, ...)
```

1.13

```python
# input and weight are dtype torch.int64
# bias is torch.float32
>>> with assertRaisesError():
>>>    out = torch.nn.functional.conv2d(input, weight, bias, ...)

# Updated code to avoid the error
>>> out = torch.nn.functional.conv2d(input, weight, bias.to(input.dtype), ...)
```

## Autograd

### Disallow setting the `.data` of a tensor that `requires_grad=True` with an integer tensor (#78436)

Setting the  `.data` of a tensor that `requires_grad` with an integer tensor now raises an error.

1.12.1

```python
>>> x = torch.randn(2, requires_grad=True)
>>> x.data = torch.randint(1, (2,))
>>> x
tensor([0, 0], requires_grad=True)
```

1.13

```python
>>> x = torch.randn(2, requires_grad=True)
>>> x.data = torch.randint(1, (2,))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: data set to a tensor that requires gradients must be floating point or complex dtype
```

### Added variable_list support to ExtractVariables struct (#84583)

Prior to this change, C++ custom autograd Function considers tensors passed in TensorList to not be tensors for the purposes of recording the backward graph. After this change, custom Functions that receive TensorList must modify their backward functions to also compute gradients for these additional tensor inputs. Note that this behavior now differs from that of custom autograd Functions in Python.

1.12.1

```cpp
struct MyFunction : public Function<MyFunction> {
    static Variable forward(AutogradContext* ctx, at::Tensor t, at::TensorList tensors) {
      return 2 * tensors[0] + 3 * t;
    }

    static variable_list backward(
        AutogradContext* ctx,
        variable_list grad_output) {
      return {3 * grad_output[0]};
    }
};
```

1.13

```cpp
struct MyFunction : public Function<MyFunction> {
    static Variable forward(AutogradContext* ctx, at::Tensor t, at::TensorList tensors) {
      return 2 * tensors[0] + 3 * t;
    }

    static variable_list backward(
        AutogradContext* ctx,
        variable_list grad_output) {
      return {3 * grad_output[0], 2 * grad_output[0]};
    }
};
```

### Don't detach when making views; force kernel to detach (#84893)

View operations registered as CompositeExplicitAutograd kernels are no longer allowed to return input tensors as-is. You must explicitly create a new tensor (e.g., using `.alias()`).

1.12.1

```cpp
torch::Tensor view_op(const torch::Tensor& self) {
  return self;
}
```

1.13

```cpp
torch::Tensor view_op(const torch::Tensor& self) {
  return self.alias();
}
```

## ONNX

### `torch.onnx.register_custom_op_symbolic` now only registers the symbolic function at the specified opset version (#85636)

This updates `register_custom_op_symbolic`'s behavior to *only register the symbolic function at a single version.* This is more aligned with the semantics of the API signature. Previously the API registers a symbolic function to *all* versions up to the specified version. As a result of this change, users will need to register a symbolic function to the exact version when they want to override an existing symbolic function. Users are not affected if (1) an implementation does not exist for the op, or (2) the symbolic function is already registering to the exact version for export.

1.12.1

```python
# Assuming an implemented symbolic function `custom_op_function`
torch.onnx.register_custom_op_symbolic("aten::foo", custom_op_function, 16)
```

1.13

```python
# Assuming an implemented symbolic function `custom_op_function`
for opset in range(1, 17):
    torch.onnx.register_custom_op_symbolic("aten::foo", custom_op_function, opset)
```

### Default ONNX opset is updated to 14 (#83284)

The update is done in regularly to ensure we are in sync with the onnx updates. Users can specify `opset_version` in `torch.onnx.export` to maintain opset version 13.

### `torch.onnx.symbolic_registry` is removed (#84382)

We removed the `symbolic_registry` module and hid it as an internal implementation detail. Users previously relying on the `register_op` function to register custom symbolic functions should move to use the `torch.onnx.register_custom_op_symbolic` API.

### `ScalarType` and global variables in `torch.onnx.symbolic_helper` are removed (#82995)

The `ScalarType` class in `torch.onnx.symbolic_helper`, along with the global variables `cast_pytorch_to_onnx`, `pytorch_name_to_type`, `scalar_name_to_pytorch`, `scalar_type_to_onnx` and `scalar_type_to_pytorch_type` are removed from the module. Users previously using these global variables for PyTorch JIT-ONNX type conversion in symbolic functions should move to use the `torch.onnx.JitScalarType` class.

1.12.1

```python
# 1
torch.onnx.symbolic_helper.scalar_type_to_onnx[
    symbolic_helper.scalar_type_to_pytorch_type.index(x.dtype)
].value

# 2
torch.onnx.symbolic_helper.scalar_name_to_pytorch[element_type] in cast_pytorch_to_onnx.keys()

# 3
torch.onnx.symbolic_helper.cast_pytorch_to_onnx["Long"]

# 4
torch.onnx.symbolic_helper.cast_pytorch_to_onnx[tensor.type().scalarType()]
```

1.13

```python
# 1
torch.onnx.JitScalarType.from_dtype(x.dtype).onnx_type()

# 2
torch.onnx.JitScalarType.from_name(element_type).onnx_compatible()

# 3
torch.onnx.TensorProtoDataType.INT64

# 4
torch.onnx.JitScalarType.from_name(tensor.type().scalarType()).onnx_type()
```

## Distributed

### **In c10d collectives, input tensors dtype must now be the same (#84664)**

We added a check to validate all dtype across all input tensors. Previously, users were allowed to pass in tensors with diferent dtypes for c10d collectives. Now, passing in tensors with different dtypes will throw a RuntimeError with the following message: “Invalid usage of tensors with different dtypes Found `torch.float` and `torch.half`”. Users can use `tensor.to(dtype={some_dtype})` to fix this.

1.12.1

```python
# users could pass inputs having different dtypes
>>> tensor = torch.ones(2, 2) * 7
>>> tensor_h = tensor.half()
>>> tensor_list = [torch.zeros(2, 2) for _ in range(4)] # Assume world_size = 4
# Both cases work.
>>> dist.all_gather(tensor_list, tensor)
>>> dist.all_gather(tensor_list, tensor_h)
...
```

1.13

```python
# all inputs of c10d collectives need to have the same dtype
>>> tensor = torch.ones(2, 2) * 7
>>> tensor_h = tensor.half()
>>> tensor_list = [torch.zeros(2, 2) for _ in range(4)] # Assume world_size = 4
# Only allow same dtype for all input tensors.
>>> dist.all_gather(tensor_list, tensor) # RuntimeError thrown
...
```

### **Users doing wildcard imports of torch.distributed.distributed_c10d will no longer get non-public symbols (#84872)**

We limit the usage of c10d APIs to public APIs, so if a user does a wildcard import and calls an internal API, it will fail. Please see the example below:

1.12.1

```python
# users could import both public and non-public symbols:
from torch.distributed.distributed_c10d import *
>>> is_nccl_available() # public API
>>> _check_single_tensor(...) # Non-public API
...
```

1.13

```python
# users can only import public symbols
from torch.distributed.distributed_c10d import *
is_nccl_available() # public API
_check_single_tensor(...) # Non-public API, this will fail now
...
```

### [Process Group C++ extensions](https://pytorch.org/tutorials/intermediate/process_group_cpp_extension_tutorial.html?highlight=process%20group) must use absolute path when importing ProcessGroup.hpp (#86257), ProcessGroup::Work object moved out of work to its own Work class (#83680):

Details of the changes and the updated tutorial can be found in the PyTorch tutorial PR [#2099](https://github.com/pytorch/tutorials/pull/2099)

1.12.1

```cpp
// users use relative path to import C++ headers and Work resides in ProcessGroup class
#include <c10d/ProcessGroup.hpp>
#include <c10d/Store.hpp>
#include <c10d/Types.hpp>
#include <c10d/Utils.hpp>
...
class WorkDummy : public ProcessGroup::Work {
    ...
}
```

1.13

```cpp
// users must use absolute path of import C++ files and Work is its own class
#include <torch/csrc/distributed/c10d/ProcessGroup.hpp>
#include <torch/csrc/distributed/c10d/Store.hpp>
#include <torch/csrc/distributed/c10d/Types.hpp>
#include <torch/csrc/distributed/c10d/Utils.hpp>
...
#include <torch/csrc/distributed/c10d/Work.hpp>
class WorkDummy : public Work {
    ...
}
```

## Quantization

### Add required `example_args` argument to `prepare_fx` and `prepare_qat_fx` (#249) (#77608)

We added an additional required `example_inputs` argument to `prepare_fx` and `prepare_qat_fx` APIs, this can be used to do type inference to figure out the type information for each of the fx Node in the graph.

1.12.1

```python
m = resnet18(...)
m = prepare_fx(m, qconfig_dict)
# or
m = prepare_qat_fx(m, qconfig_dict)
```

1.13

```python
m = resnet18(...)
m = prepare_fx(m, qconfig_dict, example_inputs=(torch.randn(1, 3, 224, 224),))
# or
m = prepare_qat_fx(m, qconfig_dict, example_inputs=(torch.randn(1, 3, 224, 224),))
```

### Stop moving models to CPU in quantization convert (#80555)

Previously, we automatically moved the model to CPU in `torch.ao.quantization.fx.convert` to work around the issue where certain functions called by convert expect CPU arguments. This commit pushes this responsibility to the caller since it is the user's decision of which device to use.

1.12.1

```python
model = resnet18(...)
model = prepare_fx(model, qconfig_mapping, example_inputs)
# calibrate
model = convert_fx(model)
```

1.13

```python
model = resnet18(...)
model.cpu()  # if needed
model = prepare_fx(model, qconfig_mapping, example_inputs)
# calibrate
model = convert_fx(model)
```

### Replace the `is_reference` flag of the `torch.ao.quantize_fx.convert_fx` function with the `convert_to_reference` function (#80091, #81326)

This PR removes the is_reference flag from the existing `convert_fx` API and replaces it with a new `convert_to_reference` function. This separates (1) converting the prepared model to a reference model from (2) lowering the reference model to a quantized model, enabling users to call their custom lowering function for
custom backends.

1.12.1

```python
from torch.ao.quantization.quantize_fx import (
    prepare_fx,
    convert_to_reference,
)

prepared = prepare_fx(model, ...)
reference = convert_to_reference(prepared, ...)
```

1.13

```python
from torch.ao.quantization.quantize_fx import (
    prepare_fx,
    convert_to_reference_fx,
)

prepared = prepare_fx(model, ...)
reference = convert_to_reference_fx(prepared, ...)
```

### Add default configs for fixed qparams ops (#80184)

This commit adds qconfigs with special observers for fixed qparams ops (operators whose corresponding quantized version has fixed quantized parameters for output) like sigmoid in `get_default_qconfig_mapping` and `get_default_qat_qconfig_mapping`. For correctness, we also require users to use these special observers if we detect these fixed qparams ops in prepare.

1.12.1 (fails after this PR):

```python
from torch.ao.quantization.quantize_fx import prepare_fx

model = ModelWithFixedQParamsOps()
qconfig_mapping = QConfigMapping()
example_inputs = ...
prepare_fx(model, qconfig_mapping, example_inputs)
```

1.13

```python
from torch.ao.quantization import get_default_qconfig_mapping
from torch.ao.quantization.quantize_fx import prepare_fx

model = ModelWithFixedQParamsOps()
qconfig_mapping = get_default_qconfig_mapping()
example_inputs = ...
prepare_fx(model, qconfig_mapping, example_inputs)
```

### Replace `qconfig_dict` with a typed `QConfigMapping` object (#78452, #79618)

Previously, FX graph mode quantization configurations were specified through a dictionary of qconfigs. However, this
API was not in line with other core APIs in PyTorch. This commit replaces this dictionary with a config object that users will
create and pass to prepare and convert. This leads to better type safety and better user experience in notebook settings
due to improved auto completion.

1.12.1 (deprecated)

```python
from torch.ao.quantization.quantize_fx import prepare_fx

qconfig_dict = {
    "": qconfig,
    "object_type": [
        (torch.nn.Linear, qconfig),
    ],
    "module_name_regex": [
        ("foo.*bar", qconfig),
    ],
    "module_name": [
        ("mod", qconfig),
    ],
}

prepare_fx(model, qconfig_dict)
```

1.13

```python
from torch.ao.quantization import QConfigMapping
from torch.ao.quantization.quantize_fx import prepare_fx

qconfig_mapping = QConfigMapping()
    .set_global(qconfig)
    .set_object_type(torch.nn.Linear, qconfig)
    .set_module_name_regex("foo.*bar", qconfig)
    .set_module_name("mod", qconfig)

prepare_fx(model, qconfig_mapping)
```

### Replace `*custom_config_dict` with typed config objects (#79066)

This commit replaces the following config dicts with python objects:

* prepare_custom_config_dict → PrepareCustomConfig
* convert_custom_config_dict → ConvertCustomConfig
* fuse_custom_config_dict → FuseCustomConfig

This leads to better type safety and better user experience in
notebook settings due to improved auto completion.
1.12.1

```python
from torch.ao.quantization.quantize_fx import prepare_fx, convert_fx

prepare_custom_config_dict = {
  "float_to_observed_custom_module_class": {
     "static": {
         FloatClass: ObservedClass
     }
  },
  "non_traceable_module_name": ["mod1", "mod2"],
  "non_traceable_module_class": [class1, class2],
  "input_quantized_idxs": [0, 1],
  "output_quantized_idxs": [0],
  "preserved_attributes": ["attr1", "attr2"],
}

convert_custom_config_dict = {
  "observed_to_quantized_custom_module_class": {
     "static": {
         FloatClass: ObservedClass
     }
  },
  "preserved_attributes": ["attr1", "attr2"],
}

model = prepare_fx(
    model,
    qconfig_mapping,
    example_inputs,
    prepare_custom_config_dict=prepare_custom_config_dict)

model(data)

model = convert_fx(model, convert_custom_config_dict=convert_custom_config_dict)
```

1.13

```python
from torch.ao.quantization.fx.custom_config import (
    PrepareCustomConfig,
    ConvertCustomConfig,
)
from torch.ao.quantization.quantize_fx import prepare_fx, convert_fx

prepare_custom_config = PrepareCustomConfig() \
    .set_float_to_observed_mapping(float_class, observed_class) \
    .set_non_traceable_module_names(["mod1", "mod2"]) \
    .set_non_traceable_module_classes([class1, class2]) \
    .set_input_quantized_indexes([0, 1]) \
    .set_output_quantized_indexes([0]) \
    .set_preserved_attributes(["attr1", "attr2"])

convert_custom_config = ConvertCustomConfig() \
    .set_observed_to_quantized_mapping(observed_class, quantized_class) \
    .set_preserved_attributes(["attr1", "attr2"])

model = prepare_fx(
    model,
    qconfig_mapping,
    example_inputs,
    prepare_custom_config=prepare_custom_config)

model(data)

model = convert_fx(model, convert_custom_config=convert_custom_config)
```

### Remove `remove_quant_dequant_pairs` and fix tests (#84203)

This PR removed some passes in `convert_fx`, and also fixes the way we quantize layer_norm operator, so the `qconfig` for layer_norm op needs to be updated as well.

1.12.1

```python
import torch
from torch.ao.quantization.qconfig_mapping import QConfigMapping, QConfig
from torch.ao.quantization.observer import default_weight_observer
from torch.ao.quantization.backend_config import (
    DTypeConfig,
    ObservationType,
)
from torch.ao.quantization.quantize_fx import prepare_fx, convert_fx

qconfig = QConfig(activation=qconfig.activation, weight=default_weight_observer)
qconfig_mapping = QConfigMapping().set_object_type(torch.nn.LayerNorm, q_config) \
.set_object_type(torch.nn.functional.layer_norm, q_config)

# assuming mymodel contains a LayerNorm layer or torch.nn.functional.layer_norm
m = MyModel()
example_inputs = (torch.rand(3, 3),)
m = prepare_fx(m, qconfig_mapping, example_inputs)
```

1.13

```python
import torch
from torch.ao.quantization.qconfig_mapping import QConfigMapping, QConfig
from torch.ao.quantization.observer import default_placeholder_observer
from torch.ao.quantization.backend_config import (
    DTypeConfig,
    ObservationType,
)
from torch.ao.quantization.quantize_fx import prepare_fx, convert_fx

qconfig = QConfig(activation=qconfig.activation, weight=default_placeholder_observer)
qconfig_mapping = QConfigMapping().set_object_type(torch.nn.LayerNorm, q_config) \
.set_object_type(torch.nn.functional.layer_norm, q_config)

# assuming mymodel contains a LayerNorm layer or torch.nn.functional.layer_norm
m = MyModel()
example_inputs = (torch.rand(3, 3),)
m = prepare_fx(m, qconfig_mapping, example_inputs)
```

### Align observer dtype with reference model spec (#85345)

Before this PR, the `dtype` attribute of observers was not clearly defined. It originally meant `interface_dtype` in the eager mode workflow, which is how the codebase before this PR is using it. In the new reference model spec, `dtype` attribute of an observer represents the `dtype` value which needs to be passed into a `quantize` function in the reference model spec. This PR aligns the codebase to this definition of `dtype`.

1.12.1

```python
dynamic_quant_observer = PlaceholderObserver.with_args(
    dtype=torch.float, compute_dtype=torch.quint8)
```

1.13

```python
dynamic_quant_observer = PlaceholderObserver.with_args(
    dtype=torch.quint8, compute_dtype=torch.quint8)
```

## Composability

### **Changed the backend C++ kernel representation for some operators that take in lists of tensors (#73350)**

If an operator in ATen takes in a list of tensors, and is marked as “structured” in native_functions.yaml ([example](https://github.com/pytorch/pytorch/blob/c8889f4e109866610bd1981f03deee8f102b5ce6/aten/src/ATen/native/native_functions.yaml#L1205)), then previously, TensorList was represented as `at::TensorList`, or `c10::ArrayRef<at::Tensor>`. Now, it is represented as a more efficient type: `const ITensorListRef&`.

1.12.1

```cpp
at::Tensor cat_kernel(at::TensorList tensors,int64_t dim) {
    ...
}
TORCH_LIBRARY_IMPL(aten, dispatch_key, m) {
    ...
    m.impl("cat", &cat_kernel);
}
```

1.13
```cpp
at::Tensor cat_kernel(const at::ITensorListRef& tensors,int64_t dim) {
    ...
}
TORCH_LIBRARY_IMPL(aten, dispatch_key, m) {
    ...
    m.impl("cat", &cat_kernel);
}
```

## C++ API

### **Lowered randint default dtype to the C++ API (#81410)**

Prior to 1.13, the default for the `dtype` argument of `torch.randint`, `torch.long`, was set via manual python binding. However, in the C++ API, `torch::randint` would default to the global default data type, which is usually `float`. In 1.13 we changed the default for `dtype` in the C++ API to `int64` in order to match the python API. To reproduce the old behavior, one can set the `dtype` argument.

1.12.1

```cpp
torch::randint(/*low=*/0, /*high=*/10, {2, 3});
```

1.13

```cpp
// assuming default dtype is float
torch::randint(/*low=*/0, /*high=*/10, {2, 3}, torch::kFloat);
```

### **Enabled `dim=None` for `torch.{std, var, std_mean, var_mean}` (#81845, #82765, #82912)**

Prior to 1.13, a C++ API call that has argument types `torch::{std, var, std_mean, var_mean}(Tensor, OptionalIntArrayRef, int64_t, bool)` used to resolve to the `{std, var, std_mean, var_mean}.correction` overload. In this release, it resolves to the `{std, var, std_mean, var_mean}.dim` overload. With the `.correction` overload, the third argument of type `int64_t` could be used to pass a correction *δN* other than 1. In order to call the `{std, var, std_mean, var_mean}.correction` overload in 1.13, the old `int64_t` argument can be wrapped in a `c10::optional`.

1.12.1

```cpp
// using std as an example
int64_t correction = 2;
torch::std(t, /*dim=*/dim, /*correction=*/correction, /*keepdim=*/True);
```

1.13

```cpp
// To replicate in 1.13 using std as an example
auto correction = c10::make_optional<int64_t>(2);
torch::std(t, /*dim=*/dim, /*correction=*/correction, /*keepdim=*/True);
```

# Deprecations

## Distributed

We are deprecating the following APIs of c10d: `*_coalesced` APIs (#85959), `*_multigpu` APIs (#85961) and `ProcessGroupRoundRobin` (#85158)

We added warnings when users call c10d’s `*_coalesced`, `*_multigpu` and `ProcessGroupRoundRobin` APIs. Previously, users can use these APIs without any warnings but now they will see warnings like “torch.distributed.all_reduce_coalesced will be deprecated. If you must use it, please revisit our documentation later at [https://pytorch.org/docs/master/distributed.html#collective-functions”](https://pytorch.org/docs/master/distributed.html#collective-functions%E2%80%9D). There are still workarounds for `*_coalesced` APIs but no workarounds will be provided for the other two.

1.12.1

```python
# users could use the following APIs with no warnings:
all_reduce_coalesced(...)
all_gather_coalesced(...)
broadcast_multigpu(...)
all_reduce_multigpu(...)
reduce_multigpu(...)
all_gather_multigpu(...)
reduce_scatter_multigpu(...)
...
```

1.13

```python
# users can still use these APIs but it will come with warnings:
all_reduce_coalesced(...)
# Warnings:
# torch.distributed.all_reduce_coalesced will be deprecated. If you must
# use it, please revisit our documentation later at
# https://pytorch.org/docs/master/distributed.html#collective-functions"

# Potential workaround:
reqs = []
with dist._coalescing_manager(group, reqs):
    reqs.append(dist.all_reduce(tensor1, async_op=True))
    reqs.append(dist.all_reduce(tensor2, async_op=True))
for req in reqs:
    req.wait()
...
```


We are deprecating passing `optim_input` into the FSDP optimizer state checkpointing APIs. The user can simply not pass the `optim_input` argument, and all behavior is preserved. No fix is needed from users side for now.

1.12.1

```python
# the user can use the following APIs with no warnings
full_optim_state_dict(...)
sharded_optim_state_dict(...)
shard_full_optim_state_dict(...)
flatten_sharded_optim_state_dict(...)
scatter_full_optim_state_dict(...)
rekey_optim_state_dict(...)
```

1.13

```python
# users can still use these APIs, but they will come with warnings
# The `optim_input` argument is deprecated and will be removed after PyTorch 1.13.
# You may remove it from your code without changing its functionality.
```

## LinAlg

### Deprecate torch.lu in favor of linalg.lu_factor (_#77636_)

The new operation has a cleaner API and better docs. The update rule is as follows:

1.12.1

```python
LU2, pivots2, info = torch.lu(A, compute_pivots, get_infos=True)
LU1, pivots1, info = torch.lu(A, compute_pivots)
```

1.13

```python
LU2, pivots2, info = torch.linalg.lu_factor_ex(A, compute_pivots)
LU1, pivots1 = torch.linalg.lu_factor(A, compute_pivots)
```

### Deprecate torch.lu_solve in favor of linalg.lu_solve(_#77637_)

The new operation has a notation consistent with `linalg.solve`, and has an extra parameter `adjoint=False`. The update rule is as follows:

1.12.1

```python
X = torch.lu_solve(B, LU, pivots)
```

1.13

```python
X = linalg.lu_solve(LU, pivots, B)
```

## ONNX

### Monkey patched convenience method on `torch._C.Graph`, `torch._C.Block` and `torch._C.Node` are deprecated. (#83006)

Deprecated methods include `Graph.op()`, `Graph.constant()`, `Graph.at()`, `Block.op()`, and `Node.__getitem__()`. Previously, these methods are patched into the classes above when users call `torch.onnx.export()` and are typically used in custom symbolic functions. Users can continue to expect `g.op()` and `g.at()` in symbolic functions to work. The `g` parameter has been substituted by the `GraphContext` object (#84728). The methods are now exposed by the `GraphContext` class with APIs unchanged. Users should not rely on the `Graph.op()`, `Graph.constant()`, `Graph.at()`, `Block.op()`, `Node.__getitem__()` methods when they are directly interacting with the C classes. Users should use only the `op()` and `at()` methods of the `GraphContext` object, as other fields in the class will change in future releases.

# New features

## Python API

* Added a deterministic implementation of `scatter_add` on CUDA for all input sizes (#79466)
* Added `torch.concatenate` that aliases `torch.cat` (#85073)
* Added `Tensor.is_cpu()`  that returns whether a tensor is on CPU (#78887)
* Added a `force` kwarg to `Tensor.numpy()` that enables returning a numpy `ndarray` that does not share storage with the tensor (#78564)
* Added `torch.special.{airy_ai, bessel_j0, bessel_j1, bessel_y0, bessel_y1, modified_bessel_i0, modified_bessel_i1, modified_bessel_k0, modified_bessel_k1, scaled_modified_bessel_k0, scaled_modified_bessel_k1, spherical_bessel_j0}` (#78900), (#78901), (#78902), (#78912),  (#78451)
* Added `torch.special.{chebyshev_polynomial_t, chebyshev_polynomial_u, chebyshev_polynomial_v, chebyshev_polynomial_w, hermite_polynomial_h, hermite_polynomial_he, laguerre_polynomial_l, legendre_polynomial_p, shifted_chebyshev_polynomial_t, shifted_chebyshev_polynomial_u, shifted_chebyshev_polynomial_v, shifted_chebyshev_polynomial_w}` (#78196), (#78293), (#78304),  (#78366), (#78352),  (#78357)
* Added `weights_only` option to `torch.load` that restricts load to state_dict only, enabling safe loading. This can  also be set using the `TORCH_FORCE_WEIGHTS_ONLY_LOAD` environment variable (#86812)

## Build

* Added `-Werror=unused-but-set-variable` build flag (#79305)
* Added ability to get release versions based on the current tag (#78584)
* Added `-Werror=type-limits` in Bazel CPU build (#79139)
* Added `-Werror=unused-variable` in Bazel CPU build (#79156)
* Added —config=shell to bazelrc file for easier debugging (#79350)
* Added clang `-Wconstant-conversion` to catch errors detected in #75400 (#80461)
* Added `-Werror=non-virtual-dtor` build flag (#81012)
* Turned on pocketfft flag for third-party pocket_fft library (#81670)
* Updated NCCL to v2.13.4-1 (#82775)
* Added `-Wunused-local-typedef` build flag (#86154)
* Increased max python version to include 3.10 (#84815)

## Complex

*  Added complex half support for:
    * [CPU] `torch.{index_select, index_add} `(#79217), (#79897).
    * [CUDA]  `torch.roll` (#79970), `torch.fft.{fftshift, ifftshift}` (#79970), `torch.{acos, acosh, asinh, atanh}`, (#80030), `torch.{cos, sinh, cosh, tanh}` (#78718), `torch.sqrt, rsqrt` (#77490), `torch.{triu, tril, diag, trace}`(#78062).
    * [CPU and CUDA] `torch.where` (#78665), `torch.{where, pow, masked_fill, sgn, tan, angle}`(#78665)
* Added complex support for `torch.nn.ConvTranspose1d` (#79694).

## torch.nn

* Added `pop` function to `nn.Sequential` and `nn.ModuleList` (#81601)
* Added deepcopy support for parametrized `nn.Module` (#80811)

## torch.optim

* Added maximization support via the `maximize` kwarg for `optim.SparseAdam` (#80336), `optim.ASGD`  (#81875), `optim.Rprop` (#81864), `optim.RMSprop` (#80326)
* Added support for differentiable optimizers via the `differentiable` kwarg `optim.SGD` (#80938), `optim.Adam` (#82205), `optim.RMSprop` (#83578)
* Added support for complex number for `optim.Adam` (#80279), `optim.AdamW` (#80280), `optim.Adamax` (#80319), `optim.RMSprop` (#83860), `optim.Rprop` (#83858),
* Handled complex params as independent real params in `optim.{RMSprop, ASGD}` (#83860), (#84472)
*  Added `optim.lr_scheduler.PolynomialLR` (#82769)

## BetterTransformer

* Allowed user to assert no mask contiguous check is necessary (#82533)
* Added support for norm_first in nn.TransformerEncoderLayer fast path (#78269)
* Added ustom scaled dot product implementations dense (#85984)
* Added Better Transformer fastpath diagnostics (#81013)

## ForEach

* Implemented inplace `foreach` `maximum` and `minimum` (#82523)

## LinAlg

* Added `linalg.lu_solve`, `linalg.solve_ex`, `linalg.vecdot`, `linalg.vander` (_#77634_, _#80073_, _#70542_, _#76303_)

## Sparse

* Added `torch.sparse.spdiags` for easier creation of diagonal sparse matrices (#78439)

## torch.fx

* Enabled symbolic shapes (#82063, #82317, #82209, #83380, #85808, #84113, #84829, #84918, #85185, #85261, #85260, #85754, #85768, #86050, #86098, #86067)
* Created an improved version of subgraph matcher (#82090, #82853, #85444, #85456, #85617)
* Rewrite subgraph_rewriter with subgraph_matcher (#83717)
* Added PassBase for writing passes, PassResult for the return value of passes, and a PassManager for managing the workflow of passes (#79878, #81366, #80531, #82485, #83933, #84094, #84425, #84232)
* Added an FX graph partitioner and fuser (#79439, #80292)
* Added a reinplacing FX pass (#80897, #83626, #83845, #83846)
* Added a CSE pass to the common passes (#81512, #81530, #81742)
* Created DecompositionInterpreter for decomposing aten → prims after an initial make_fx call (#79989)
* Created a Backend for NvFuser based graph partitioner + Prims (#80591, #81311, #81436, #81911)
* Created a Backend for Cudagraphs from dynamo (#80566)
* Created a type constraint generator to Z3 (#79912, #80084, #80095, #80102, #80110, #80147, #80744, #80799, #80823, #80847, #80909, #80925, #80976, #81159, #81175, #81189, #81190, #81265, #81274, #81344, #81360, #81376, #81445, #81516, #81527, #81714, #82163, #82590, #82597, #82614, #82742, #82856, #82923,#82938,#83087, #83109, #83194, #83334, #83682, #83945)

## JIT

* Added new NVFuser Python Frontend Record Keeping for Cache enablement. (#81578)
* Added `torch.ops.nvprims` namespace for nvFuser-specific prims (#82155)
* Enabled fusion of conv with elementwise OP in NNC (#77157)
* Added symbolic shape functions for `conv_transpose2d.input, convolution, convolution_backward` (#77283, #83557, #80860)
* Added support in symbolic shapes for generalized lists of tensor shapes, tuple outputs, optional None, upper and lower bounds (#77389, #83092, #83222, #78679)
* Added support for `aten::_convolution` when it is 2D conv in NNC (#84038)
* Exposed `ProcessGroup::Work.wait()` API to TorchScript (#83303)

## ONNX

* Inlined `prim::PythonOp` for Autograd Function Export (#74765)

## AMD

* Enabled nvfuser (#82498)

## CUDA

* Added CUDA trace Python hooks (#82824)
* Added CUDA Sanitizer (#83984)
* Added support for multiple outputs in python jiterator  (#77921, #78139)

## Intel

* Added a launch script with Best Recipe of Deep Learning on Intel Xeon CPU (_#63932_)
* Enabled Intel® VTune™ Profiler's Instrumentation and Tracing Technology APIs (ITT) to PyTorch (_#63289_)
* Added unified x86 quantization backend (_#84329_)

## MPS

* Added `aten::index_add.out` operator for MPS backend (_#79935_)
* Added `aten::prelu operator` for MPS backend (_#82401_)
* Added `aten::bitwise-not` operator native support for MPS backend (_#83678_)
* Added `aten::tensor::index_put` operator for MPS backend (_#85672_)
* Added `aten::upsample_nearest1d` operator for MPS backend (_#81303_)
* Added `aten::bitwise_{and|or|xor}` operators for MPS backend (_#82307_)
* Added `aten::index.Tensor_out` operator for MPS backend (_#82507_)
* Added `aten::masked_select` operator for MPS backend (_#85818_)
* Added `aten::multinomial` operator for MPS backend (_#80760_)

## Profiler

* Integrated Execution Graph Observer into PyTorch Profiler (#75358, #79753, #82895, #84285)
* TorchTidy: experimental tool to identify anti-patterns from traces (#79631, #79874, #79993, #80094, #80108, #80572, #81056, #81273, #81501, #81733, #81740, #81921, #82421, #82248, #82261, #82782)
* Added reporting for OOM events to the Pytorch Profiler. (#80050)

## Vulkan

* Added Vulkan support for the following operators:
    * `torch.cumsum` (#78554, #81107)
    * `torch.nn.LSTM` (#78943, #79702)
    * `torch.nn.ReplicationPad2d` (#79057, #79291)
    * `torch.nn.threshold` (#78654, #79717)
    * `torch.nn.BatchNorm2d` (#80510)
    * `torch.nn.LayerNorm` (#80980)
    * `torch.nn.GLU` (#80910, #81729)
    * `torch.select` (#81771)
    * `torch.stack` (#81064)
* Prototype implementations for Quantized Tensors were added (#81491). These implementations still need to be exposed to Torchscript, but so far prototype implementations for the following ops have been added:
    * `torch.quantize_per_tensor` (#81492)
    * `torch.dequantize` (#81493)
    * Quantized arithmetic ops (#81494, #81632, #81640, #81641)
    * Quantized 2D convolution (#81495, #81496, #81497)
    * Quantized `Upsample2D` (#81720)

## Mobile

* Added support for dtypes and custom classes in model tracer (#84795)
* Extended Flatbuffer to get mobile_info for NMLML workflows (#78306)
* Added serialization/deserialization of Sparse Quantize Linear Packed Params (#80474)
* Added qnnpack bcsr matrix unpacking and use unpacking in Linear module (#80475)
* Added OwnedOrBorrowedVector for QNNPack BCSR Indices/Values (#80476)

## Distributed

#### `Distributed Checkpointing` (Prototyping)
* This is a prototyping effort which enables loading and saving PyTorch models from one or more hosts. Models can use features such as DDP, FSDP and ShardedTensor and they can have a different configuration between saving and loading - for example, save from 4 hosts and load from a single host. Distributed checkpointing has an extensibility API that enables full control of how a model is saved; and a pluggable IO backend. (#83781, #83419, #84952, #84881)

#### `Distributed(c10d)`

* Made c10d collective ops dispatcher passable. It allows tracing mechanisms such as LazyTensor and AOTAutograd to observe communications, e.g., : broadcast(#76722), allreduce(#79582), allgather (#79669), reduce_scatter (#79683), reduce  (#79686), gather (#79687), scatter (#79688), alltoall (#79691), barrier (#79777), send/recv (#79779).
* Added UCC process group (#79918)
* Enabled uneven input support for `all_gather`  (#83713) and uneven output support for `reduce_scatter` (#87010)
* Added NCCL PreMul Sum to c10d `ReduceOp` (#84243)

**`DistributedDataParallel`**

* Made DDP work with Python process group (#79176)
* Enabled Zero1's ddp_with_overlap for hpu backend (#80438)

#### `FullyShardedDataParallel`

* Added forward prefetching option in FSDP API (#85177)
* Added fp16 and bf16 hooks for FSDP (#81711)
* Implemented `sharded_optim_state_dict` and `flatten_sharded_optim_state_dict`. (#77628)
* Added rate limiter (#83917) Thanks to IBM Research team, @lchu-ibm for his contributions to FSDP and @hfwen0502 for the experimental testbed that identified the issues.
* Added an option to keep grads in lower prec (#85223)

#### `torch.distributed.elastic`

* Added watchdog to TorchElastic agent and trainers (#84081)

#### `Activation Memory Management` (Prototyping)

* We offer a new API, `torch.distributed.algorithms.checkpoint.checkpoint_wrapper` to wrap `nn.Modules` with activation checkpointing or activation offloading to easily use and experiment with activation checkpoint techniques without modifying model code. This makes it simpler to leverage activation checkpointing to reduce memory footprint of your training applications and train larger models. (#83035, #78704, #78854, #79830, #80089, #84907, #84908, #85448, #85449)

## Infra (RelEng)

* Enabled multigpu unittests on FSDP (#77947)
* Added feature to do rebase (via comment) onto any branch (#78772)
* Added implementation to allow PR collaborators to revert their PRs (#82360)
* Added torchvision onto the commit pins file (#79151)
* Turned on `-Werror=all` with a few exceptions in Bazel build for CUDA (#79306)
* Prepared for running PyTorch tests with TorchDynamo and skips for known failing tests (#80106)
* Added ROCm build to pull request jobs (#80149)
* Added dynamo test configuration (#80342)
* Enabled ROCm CI for trunk test (#80920)
* Added linux cuda 11.7 workflows (#81089)
* Updated CI docker images and jobs to ROCm5.2  (#81168)
* Added UCC PG build in CI (#81583)
* Enabled periodic builds for CUDA 11.7 (#81688)
* Enabled distributed tests for ROCm (#81751)
* Added New TORCH_UCC_BLOCKING_WAIT env variable (#81791)
* Change functorch pin mechanism to test functorch in pytorch/pytorch now that functorch is inside pytorch/pytorch (#81918)
* Added Python 3.11 nightlies for Linux PyPi (Please note that 3.11 binaries are not fully functional) (#82302)
* Updated ROCm nightly builds to rocm5.2 (#82353)
* Add functorch target to cmake (#83464)
* Upgraded CUDNN version for cuda 11.7 (#84964)
* Enabled pytest-shard for functorch (#85321)
* Enabled CI to run test_ops in parallel (#85528)
* Updated trunk CUDA-10.2 to CUDA-11.7 (#85943)
* Added support for building and running Metal tests in CI (#86073)
* Bumped nvidia docker version and using python 3.10 for cuda11.7 (#82472)

# Improvements

## Python API

* Added `float16` support for `torch.{arange, linspace}` (#80492)
* Added integer support to `torch.index_reduce` (#80464)
* Added a `stable` kwarg to `torch.argsort`  that controls the relative order of equivalent elements (#75162)
* Improved stability of `torch.distributions.kl_divergence`  for two Bernoulli distributions (#79944)
* Improved type annotations for `torch.{as_tensor, as_subclass}`  (#86105)
* Added type promotion support for `torch.{addcmul, addcdiv}` (#74234)
* Added `bfloat16` support for `torch.save` with XLA/HPU tensors (#77534)
* Improved wrapper subclass detection for serialization (#81105)
* Updated python API `TensorOption` signatures for consistency with JIT schemas (#82241)
* Allowed disabling of`torch.library.Library` with PYTORCH_DISABLE_LIBRARY (#85190)
* Enabled `dim=None` for `torch.{mean, sum, nanmean, nansum}` (#81286), (#79881), (#82912)
* Added feature to enable registration of extension device modules as a native module under the torch namespace (#78329)
* Added `logsumexp` to `amp.autocast` (#76330)

## C++ API

* Allowed `const T&` access to `ListElementReference` (#83177)
* Redirected print messages to `stderr` in `torch.utils.cpp_extension` (#82097)
* Updated CUDA compiler matrix in `torch.utils.cpp_extension` (#82860)
* Added `__all__` to `torch.utils.cpp_extension`, `torch.utils.hooks` and `torch.utils.show_pickle` (#85331)

## Autograd

* Added forward AD coverage for `torch.{amin, amax, nansum, nanmean}`  (#80082),  `torch.scatter_reduce` (except `reduction=prod`) (#85000),  `torch.linalg.det` (#79487),  `torch.{elu_, celu_, selu_}` (#83080)
* Added forward-over-reverse AD coverage for `nn.functional.{binary_cross_entropy} `(#77852) , ` nn.functional.{embedding} `(#79699),` nn.functional.{mse_loss, softplus, l1_loss, smooth_l1_loss, prelu, hardswish}` (#78740), `nn.functional.{nll_loss,  batch_norm, layer_norm, group_norm, cross_entropy, soft_min}`  (#84976) `torch.`{`log_softmax, softmax}`(#84976), `torch.amin, amax, nansum` (#80082)
* Added support a stable double backward on `torch.linalg.det` for real inputs (#80217)
* Added support for kwargs input to function when `torch.utils.checkpoint` with `use_reentrant=False` (#80987)
* Added context manager to disable saved tensor hooks: `torch.autograd.graph.disable_saved_tensors_hooks` (#85971)
* Added new cpp custom function API to inform the backward function whether a gradient is necessary to compute: `ctx->needs_input_grad(idx)` (#82544)
* Added all device types in the pybinded DeviceType enum (#83676)
* Added `check_nan` flag to `torch.autograd.detect_anomaly` which enables users to run anomaly mode without nan checking (#83481)

## Build

* Specify "Generic" BLAS library name to ensure PyTorch can find the BLAS llibrary (#74269)
* Generate CUDAConfig.h only for CUDA builds (#78218)
* Moved build_variables.bzl and ufunc_defs.bzl from pytorch-root/tools/ to PyTorch root directory (#78542)
* Made lintrunner compatible with M1 (#78628)
* BLAS library is linked privately instead of being linked publicly (#78883)
* Updated build targets to include generated enum_tag.cpp (#79668)
* Use miopen_LIBRARIES and rccl_LIBRARIES directly, when they are valid target for RCCL (#80446)
* Deleted Win specific case for CMake older than 3.1 (#81411)
* Split `.cu` to improve compile times (#81193)
* Added `append_cxx_flag_if_supported` macro (#82883)

## torch.nn

* Improved `groups` argument validation for `nn.Conv{1,2,3}d` modules (#77919)
* Improved error message for convolution backward fallback kernel (#81538)
* Reduced memory usage of `nn.Module` full backward hooks by removing reference cycles (#80139)
* Improved `kl_div` at boundary and its general implementation (#80334)
* Improved input shape validation for MKL-backed convolution operations (#76526)
* Improved input validation for `nn.AdaptiveAvgPool2d` (#84061)
* Improved `groups` argument validation for `nn.Conv{1,2,3}d` (#85248)
* Improved input index validation for `nn.MaxUnpool{2,3}d` (#78280)
* Improved listing of public APIs for `optim` and `nn` (#80237)
* Added new operator for `nn.Sequential`: `+` (#81170), `extend` (#81179), `insert` (#81402), `+=`, `*` and `*=` (#81279),
* Added deepcopy support for unitialized parameter (#83809)
* Added nondeterministic alert for `nn.MaxUnpool`{`1,2,3}d` (#84766)
* Added Bfloat16 support for the backward pass of `nn.functional.kl_div` on CUDA (#77676)

## torch.optim

* Added support for optimizers with more than 2 betas for LRScheduler (#84486)
* Added `fused` kwarg to `optim.Adam` to enable a fused implementation on CUDA (#85739)

## Composability

* Significant hardening and improvements to the `functionalize()` API that lives with functorch (#77129, #77126, #77125, #78199, #77132, #77713, #77714, #78819, #78820, #82008, #82009, #81702, #80416, #80418, #80251, #80526, #82326, #81454, #81471, #83542, #83701, #85975)
* Allow `__torch_dispatch__` subclasses and modes to override more tensor metadata: device/size/stride/dim (#77684, #77970, #78646, #78691)
* Improvements to the `torch.library` API, for registering python functions to the pytorch dispatcher:
    * Improved error checking in `torch.library` (#77990)
    * Make `torch.library` decorators return function, to allow for chaining (#78996)
* Ported `cholesky`, `linalg_qr`, `linalg_eigh` and `linalg_eighvalsh` to structured kernels, giving them support with meta tensors (#79300, #79054, #79072)
* Added python decompositions for many torch operators. This adds meta tensor coverage for a large number of pytorch operators (#77930, #79768, #79808, #84062, #84350, #80219, #78350, #79667, #81003, #81420, #81113, #81241, #81765, #82284, #80497, #80358, #80182, #80737, #81734, #81826, #78461, #78468, #78525, #78914, #78919, #79900, #79225, #80964, #83235, #84108, #84451, #78602, #78603, #78527, #78604, #78992, #78993, #78997, #79278, #79341, #79311, #79411, #79581, #81800, #79834, #82309, #79975, #82587, #82603, #83191, #84349, #84460, #85793, #86057)
* Beefed up API for printing out operators registered to the dispatcher (#78995)
* Trued up `c10::FunctionSchema::operator<<` to print native_functions.yaml syntax (#79645)
* Made it so that it is valid to set metadata after detach calls, like `x.detach().resize_(...)` (#83590)
* Optimized `torch.ops.ns.opname.overload` accessor in `__torch_dispatch__` (#85132)

## Dataloader

* Added shape checking on argument `weights` for `WeightedRandomSampler` (#78585)
* Added support for `radom_split` to accept percentages as `lengths` (#78877)
* Extended collate function that can register collate functions to handle specific batch types (#85748)

## Functorch

* `functorch.jacfwd` now accepts a `randomness` kwarg (#84220)
* Improved the error message when using `vmap` on a function with no Tensor inputs (#83016)
* Relaxed the `Tensor.as_strided` batching rule. This is a primitive used in forward-mode AD (among other things) and improves composability of vmap with other transforms (like jvp).
* `functorch.functionalize`: added support for in-place views on inputs (#83993)
* `functorch.functionalize`: moved this API out of the `functorch.experimental` namespace (#85742)
* Added vmap support for `linalg.cholesky`, `linalg.eigvals`, `linalg.eigvalsh`, `linalg.matrix_norm`, `linalg.matrix_power`, `linalg.norm`, `linalg.tensorinv`, `linalg.solve_triangular`  (#82177)
* Added vmap support for `linalg.solve` (#82814)
* Added vmap support for `linalg.cross` (#83759)
* Added vmap support for `linalg.matrix_rank` (#83760)
* Added vmap support for `linalg.pinv` (#83761)
* Added vmap support for `Tensor.fill_` (#84015)
* Added vmap support for `linalg.lstsq` (#82325)
* Added vmap support for `linalg.lu_solve` (#85175)

## LinAlg

* Added a `driver=` kwarg to `torch.linalg.svd` and `svdvals`. Add cusolver gesvdaStridedBatched driver to `linalg.svd` (_#74521_)
* Added opteinsum backend to `torch.einsum` (_#86219_)
* Added path optimize kwarg to `einsum` (#84890)
* Call view instead of sum in `einsum` to remediate MPS regression (#87135)
* Ensure that we contract left to right in `einsum` (#87199)
* Fixed opt_einsum defaults to be more reasonable (#86985)

## Sparse

* Added `sparse_dim` and `dense_dim` for batched, hybrid CSR/CSC/BSR/BSC (#80565, #80901)
* Added support for conversion between batched CSR/CSC/BSR/BSC and dense Tensors (#80781, #83084, #83086, #78025, #80354, #82120)
    * Conversion between SparseBsr and Strided (#78025)
    * Added support for BSR <-> Strided Conversion (#80354)
* Added support for conversion between CSR and CSC (#85091)
* Added support for conversion between BSR and BSC (#85091)
* Added partial support for CSR/CSC/BSR/BSC inputs to `mm`, `addmm`, `matmul` and `F.linear` (#85551, #85308, #85379, #85307)
* Added support for COO to `permute` (#79707)
* Added support for ComplexHalf to `torch.nonzero` and `add(dense, CSR)` (#79062)
* Added support for CSC/BSR/BSC to unary zero-preserving functions. (#78173, #85031)
* Added support for batched BSR/BSC to `transpose` (#82122)
* Added support for scalar together with COO inputs to `mul` (#82962)
* Added support for CSC/BSR/BSC to `empty_like` (#82310)
* Added support for batch dims of CSR/CSC/BSR/BSC to `select` (#82119)

## torch.fx

* In constant folding, added `device_for_folded_attrs` parameter and sets the `requires_grad` option for a folded tensor (#79067)
* Mode-based tracing in make_fx (#79638, #84238)
* Made executor handle kwargs (#79858)
* Added `ignore_parameters_and_buffers` flag to FxGraphDrawer (#79982)
* Enabled an `is_fx_tracing` flag in the FX tracer (#80255)
* Attached ProxyTorchDispatchMode to ProxyTensor and use it in `__torch_dispatch__` (#82549)
* Used `enable_tracing` flag for ProxyTorchDispatchMode instead of modifying torch dispatch mode stack inner attributes (#82643)
* Improved legalize_graph pass in FX (#82874)
* Implemented `__deepcopy__` for fx.Tracer (#83130)
* Hackde up make_fx to natively support varargs (#83210)
* Updated proxy_tensor.py to support List input/output (#83302)
* Added *_only and all/any pytree utilities (#83316)
* Deleted ProxyTensor wrapper subclass (#83330, #83646)
* Added support for partial decompositions in make_fx (#83770)
* Added metadata field to fx.GraphModule (#84378)
* Added option to maintain the FX graph execution order after splitting_module (#85188)

## JIT

* Added PReLU to MKLDNN convertible Ops in JIT optimize_for_inference (#79011)
* Enabled `torch._refs.var` for nvFuser executor (#79517)
* Fixed nvFuser's `where` (tensor, python_scalar, tensor) type promotion (#80347)
* Added ComplexDouble scalar creation bindings to nvFuser's Python API (#80522)
* Added real and imag to NVFuser and its python frontend (#79824)
* Added Nvfuser opt in for decomposition (#81134)
* Added `torch.jit.fuser()` option for disabling all fusers (#81731)
* Added support for symbolic diff for `silu` (#81724)
* Added NVFuser support for (`prims.sign, refs.sign, squeeze, native_batch_norm, transpose`) (#83167, #85562, #84629, #84117)
* Use high precision accumulate buffer for bf16 accumulation in NNC (#84402)

## Quantization

* Improved quantization support for `masked_fill` (#78368, #85108)
* Improved quantization support for `index_put` (#78384, #85685)
* Improved quantization support for `LSTM` and `MultiHeadAttention` (#79959, #79956, #79960, #83304, #85068)
* Added support for quantized `matmul` (#83885)
* Introduced a more stable conv_bn fusion for QAT training (#85744)
* Removed warnings from using torch.tensor(value) (#84277)

## ONNX

* Added operator support for `torch.tensor_split` (#77437), `torch.lerp` (#78891), `torch.movedim` and `torch.moveaxis` (#78931), `torch.scatter_add` (#79103), `torch.argsort` (#80234), `aten::native_dropout` (#81743), `aten::native_layer_norm` (#81754), `aten::convolution` (#81815), `aten::_log_softmax` (#81804), `aten::layer_norm` for ONNX opset version 17 using LayerNormalization (#84293), `nn.init.normal` (#84149)
* Added quantization support to more single output ops (#83008) `aten::reshape`, `aten::reshape_as`, `aten::t`, `aten::transpose`, `aten::numpy_T`, `aten::expand`, `aten::expand_as`, `aten::embedding`, `aten::embedding_bag`, `aten::view`, `aten::select`, `aten::eq`, `aten::ne`, `aten::gt`, `aten::lt`, `aten::le`, `aten::ge`, `aten::elu`, `aten::selu`, `aten::hardtanh`, `aten::hardswish`, `aten::as_strided`, `quantized::sigmoid`, `quantized::layer_norm`, `quantized::group_norm`, `quantized::leaky_relu`, `quantized::instance_norm`
* ONNX operators are exported with names containing their associated scope from `nn.module` (#82038), (#82039), (#82040)
* Introduced runtime type checking with the beartype library in all public APIs (#83673), (#84091)
* All `torch.onnx` APIs now support runtime type checking when @beartype is present in the Python environment. A warning is emitted when a type mismatch is detected.
* This feature is experimental. To turn all warnings into errors, set the environment variable `TORCH_ONNX_EXPERIMENTAL_RUNTIME_TYPE_CHECK=ERRORS`. To disable this behavior, set `TORCH_ONNX_EXPERIMENTAL_RUNTIME_TYPE_CHECK=DISABLED` which effectively makes it a no-op.
* Improved shape type inference (#78999)
* Turn on ONNX shape inference by default (#82767)
* Enabled data propagation from ONNX (#80730)
* Introduced SARIF (#85428) for `torch.onnx` submodule
* Improved warnings and errors (#78441), (#78309), (#83332), (#85179), (#83007)
* Updated ONNX submodule to 1.12 (#79585)
* Apply Common Subexpression Elimination pass to ONNX export (#85665)

## AMD

* Support benchmark flag for MIOpen (#77438)
* Correctly handle the error codes of hipGetDeviceCount (#80405)
* Use torch._C._cuda_getArchFlags to get list of gfx archs pytorch was built for (#80498)
* `torch.cuda.is_bf16_supported()` returns True (#80410)
* Workaround missing hipProfilerStart/Stop (#82778)
* Enabled jiterator on ROCm (#77982)
* Enabled MIOpen fused convolution relu (#82002)
* Restore MIOpen benchmark flag default to true (#82656)
* embedded_interpreter_hip to enable torch::deploy on AMD (#83329)
* Add HIP libs into torch deploy init list & corresponding dependency for CURE benchmark running on AMD (#83434)

## CUDA

* Added synchronize hooks (#84427)
* Added CSAN support for CPU synchronizations (#84428)
* Return device count using nvml (#84879)
* Reworked printing tensor aliases in CSAN error message (#85008)
* Added jiterator support when dtype is `complex32` for `tan`, `atan`, `sin`, `asin` (#77802),(#77606)
* Added jiterator support when dtype is complex for `logical_{or, xor}` (#75947)
* Reduced overhead of `get_current_stream` (#78066)
* Added an argument to specify warmup iterations in make_graphed_callables (#78124)
* Small improvements to `device_count` (#85192)
* Memoize `torch.cuda.device_count` (#84878)
* Remove the construction of unused tensors in fallback convolution implementation (#79183)
* `__launch_bounds__` for `torch.mode` with CUDA 11.7 (#79710)
* Removed synchronization for D2H copy with a different dtype  (#80607)
* Added nondeterministic alert to CUDA `cumsum` (#75693)
* Annotated CUDACAchingAllocator snapshots (#82146)
* CUDACachingAllocator snapshots from C++ (#86190)
* Propagate CUDAOutOfMemoryError to Python. (#83146)
* Set cublas workspace size to 4M (#74159)
* Allow changing the cuda allocator settings even after the process started (#84970)
* Fixed exception handling, improve overheads and avoid constructing storage for element size for DLPack (#84612)
* Added BFloat16 for fast layernorm (#83971)
* Added BFloat16 support for `torch.{im2col,col2im}` on CUDA (#84372)
* Added Bfloat16 support for `ReflectionPad` (#84949)
* Added explicit `__all__` to torch.cuda (#85193)
* Set CUDA_MODULE_LOADING to LAZY when not set by the user (#85692)
* Support cuDNN Errata Filter (#73934)
* Allow the number of kernels profiled under torch.backends.cudnn.benchmark = True to be limitedCudnnv8 benchmark limit (#78299)
* Update tests and dispatching for CUDNN V8 API behavior for bfloat16 convs (#81139)

## Intel

* [RFC] Enable oneMKL&oneDNN on-demands verbose functionality (_#63212_)
* Updated ideep for NNC post-op (_#82705_)
* Enabled native 1d spatial input for Intel xpu (_#82301_)
* Added loss operators to fp32 cast policy of AutocastCPU (_#81689_)
* Added bfloat16 support for `lerp` on CPU (_#84327_)
* Added `prelu` op and module for quantized CPU backend (_#73491_)
* Enabled mkldnn matmul for aarch64 bf16 devices (#85546)

## MPS

* Added ranked tensors for addcmul ops in MPS instead of constants and update MacOS version check (_#78354_)
* Moved MPS compat check into common comparison machinery of `TensorLikePair` (_#77836_)
* Made MPS buildable with either XCode or CommandLineTools (_#79430_)
* Improved MPS `aten::softplus` operator by adding RankedPlaceholder for graph nodes instead of constants (_#81169_)
* Extended MPS Conv1D operation for NHWC format (_#83121_)
* Added support for 1D weights in MPS linear layer (_#85752_)
* Added full support for serialization of MPS Tensors (_#79465_)
* Added support for 1D bias in MPS operation `torch.addmm `(_#81519_)
* Added torch dispatch stub code for MPS backend (_#82612_)
* Use convenience helper function `dispatch1DJob` for MPS native implementations (_#82982_)
* Enabled support in MPS for `torch.adaptive_avgpool_2d` for larger output sizes (_#85726_)
* Extended support in MPS for `torch.constant_pad_nd` for 4D+ padding (_#85991_)

## Profiler

* Propagate metadata into `Engine::evaluate_function` event. (#77696)
* Switched to nanoseconds for Result's internal representation (#77697)
* Made profiler table column widths changeable via arguments (#85203)

## Vulkan

* Enabled higher dimensional input in `torch.nn.linear` (#81773)
* Vulkan tensor views now infers dim size when -1 is provided as input (#81668)
* Vulkan prepacked op contexts will now release the deserialized CPU tensors from memory upon construction (#83587)
* Vulkan shader codegen is now Windows compatible (#85241)

## Mobile

* Allowed tracing multiple input models at once (#84833)
* Leaky `relu` in metal shader (#78544)
* Added detailed error message for iOS test (#79140)
* Remove dcode duplications and refactor (#79184)
* Optionally run fbgemm in tracer (#83531)
* Added hardshrink op to metal backend (#82224)
* New flatbuffer_loader functions that do not depend on flatbuffers.h (#82618)
* Added `max_pool2d`, `linear`, `conv2d` FP32 operator tests for XNNPACK (#83131)
* Removed flatbuffer types/headers from flatbuffer_serializer[_jit].h (#82619)
* Migrated remaining pytorch code to use new flatbuffer_loader.h APIs (#82620)
* Remove flatbuffer types/headers from flatbuffer_loader.h (#82893)
* Use flatbuffer of alternate namespace (#82952)
* Hide flatbuffer build dependencies (#82953)
* Renamed flatbuffer_all to flatbuffers_jit (#82826)
* Renamed flatbuffer_serializer to *_mobile or* _full_jit  (#82827)
* Created flatbuffers_mobile (#82828)
* Added API for profiling backend memory events for Edge CPU profiler (#80350)
* Switched mobile targets to flatbuffers_mobile (#82829)
* Added an option to avoid adding base ops to static op library for Edge (#84360)
* Fixed load_extra_only api for flatbuffers and enable flatbuffers in mobile for OSS properly (#83855)
* Remove unused field 'order_' in nnapi.h (#84067)

## Distributed

#### `Distributed(c10d)`

* c10d API improvements:
    * Introduced util functions in c10d `get_local_rank`, `get_global_rank` and `get_global_ranks` (#82134, #84363)
    * Replaced internal API `_all_gather_base` with a public API `all_gather_into_tensor` (#85686)
    * Replaced internal API `_reduce_scatter_base` with a public API `reduce_scatter_tensor` (#85867)
* Improvements to c10d error messages:
    * Added `ncclGetLastError` (#83724, #85825, #85850)
    * Added closing parentheses to the CollectiveFingerprint (#79723)
    * Added tensor deserializer and included rank and collective type to the error messages (#79724)
    * Adopted `ncclRemoteError` (#85887)
* Passed group ranks and options to third party distributed backends (#73164)
* Enabled NCCL_DESYNC_DEBUG when TORCH_DISTRIBUTED_DEBUG is set to DETAIL (#83881)
* Added a soft error handling mode `NCCL_ASYNC_ERROR_HANDLING=2` that does not crash the process (#84386)
* Upgraded NCCL to 2.14.3 (#85367)

#### `Distributed Optimizer`

* Added functionality for save and restore step counter for model averanger in PostLocalSGDOptimizer (#78988)

#### `DistributedDataParallel`

* Enabled the static graph to print unused parameters in debug mode for DDP. (#81929)
* Enabled stateful PowerSGD communication hook now can be saved and reloaded to resume training (#79334)

#### `FullyShardedDataParallel`

* Allowed different `optim_input` orders across ranks (#78599)
* Added profiling range for FSDP.backward (#78479)
* Enabled NamedTuple support for FSDP (#83055)
* Added FSDP communication hook interface for NO_SHARD strategy (#79833)
* Moved the `sharded_state_dict` logic to the post hook to avoid OOM (#82613)
* Added ability to iterate through dataclasses in fsdp.utils (#82638)
* Enabled passing kwargs to load_state_dict (#83309)
* Used `_init_from_local_tensor` to create ShardedTensor to avoid communication overhead (#82911)
* Added communication hook for sharded strategies (#83254)
* Changed to print exec order only in debug mode (#83868)
* Ensured that all ranks use the same order to iterate through optimizer states (#84654)
* Optimizer states may be on CPU, copied them to GPU before gathering (#84708)
* Handled the `state_dict` on CPU cases (#85640)
* Add `FSDPExtensions` for TP support (#85039)
* Ignored buffers that are non-persistent. (#85740)
* Delayed moving tensor to CPU until necessary for optim_state_dict() (#85761)
* Dequeue one event instead of flushing for rate limit (#86165)

#### `torch.distributed.elastic`

* Implemented a named pipe based watchdog timer (#83695)

## Infra (RelEng)

* Consolidated all python targets in the tools folder (#80408)
* Improved ios simulator test in CI (#80459)
* Add functorch testing shard in CI (#81283)
* Added functorch shards for windows CI (#82161)
* Added functorch shard for mac x86 tests, linux cu102 tests (#82000)
* Added CI workflow to build official docker images with multiarch (#83437)
* Sharded `trunk / linux-bionic-cuda10.2-py3.9-gcc7 / test (default` from 2 -> 4 (#83424)
* Migrated workflows from 18.04 to 22.04 (#83861)



# Bug fixes

## Python API

* Fixed `dim` out of range check for `logcumsumexp` on CUDA when the source tensor is empty(#78284)
* Added missing `__init__.py` for `torch.utils.jit` (#78629)
* Fixed backward crash for `gather` with an empty index tensor when `sparse_grad=True` (#78698)
* Added type annotations to `torch.distributions.kl_divergence` (#78432)
* Fixed erroneous inclusion of `end` in the output of `torch.arange` for some inputs (#80758)
* Fixed `torch.distributions.Transform` to be pickle-able (#81707)
* Added check that `self` and `mask` are on the same device for `torch.masked_fill` (#82737)
* Fixed potential ref cycle creation in `torch.utils.checkpoint` (#82776)
* Fixed `Tensor.__hash__` for Tensor subclasses (#83174)
* Fixed `torch.cat` for 0-dim tensors with different dtypes (#83391)
* Fixed `torch.equal` on CPU when inputs have different dtypes (#83350)
* Fixed data-dependent shapes in `torch.districutions.{HalfCauchy, HalfNormal}` (#84322)
* Added check that the size of the last dimension of `tau` is less than or equal to that of `input` in `torch.ormqr`  (#85278)
* Added check that `weights` is a 1D tensor in `torch.bincount` (#85881)
* Fixed segfault for `out` arguments that have a large number of dims (#85294)
* Fixed comparison ops with scalar arguments by removing overflow check (#78881)
* Normalized `torch.utils.dlpack` strides to 1 where size of corresponding dimensions < 2 (#83158)
* Added a check in `torch.empty_strided` that `sizes` has the same dimensionality as `strides` (#82422)
* Fixed `torch.istft` default output length to prevent trimming of last element (#80031)

## C++ API

* Fixed missing antialiasing path to the interpolation for bicubic mode (#84599)
* Added `IListRefTag::Materialized` to `IListRefIterator` destructor. (#85467)
* Fixed `im2col` by adding a check that `pad_width` and `pad_height` are non-negative (#85541)
* Fixed `check_compiler_ok_for_platform` on non-English locales in `torch.utils.cpp_extension` (#85891)

## Autograd

* Corrected the forward AD formula of `torch.sgn` which fixed forward-over-backward for `torch.linalg.svd `and other spectral decompositions, and `torch.norm`, `torch.linalg.{norm, matrix_norm}`(#80082)
* Fixed derivatives of convolution overridable backward (#80840)
* Updated setting non-float non-complex values for forward AD dual tensor to properly error(#78361)
* Fixed forward AD to not set tangent as-is in some situations (#79664, #79653)
* Fixed cpp hooks, retains grad, and `backward(inputs=)` behavior in-place (#79996)
* Relaxed storage layout checks for forward AD when zero-numel tensor (#81055)
* Fixed leak when `create_graph=True` and full backward hook registered (#82788)
* Fixed view and in-place interaction when grad_fn is first accessed in no-grad mode (#83872)
* Updated backward of `torch.stack` to correctly handle implicit real->complex casting (#84993)
* Fixed gradients for `torch.nn.functional.{leaky_relu, threshold}` when inplace=True (#85634)
* Corrected autocasting behavior in  `torch.utils.checkpoint` when use_reentrant=False (#81766)
* Fixed gradcheck when outputs that don't require grad precede those that do (#77743)
* Fixed backward and double backward for `nn.functional.binary_cross_entropy_with_logits` (#80083)
* Fixed derivatives of `norm(p=inf)` (#78105)
* Fixed forward AD when conj-ness of primal and tangent of the dual tensor tensor do not match (#78358)

## Build

* Use C++17 for RocksDB 7 header. (#75741)
* Fixed Windows builds with _DEBUG flag (bbe8d019f2)
* Pass WITH_BLAS option from environment to CMake (#78037)
* Remove `-Wno-unused-but-set-variable` for clang 13.0.0 (#79666)
* Fixed variable typo for USE_SYSTEM_PYBIND11. (#80272)
* Fixed compilation errors during build with clang13 (#80916)
* Added missing -fexceptions flags during PyTorch build (#81394)
* Fixed CMake dev warning (#81580)
* Fixed false positive AVX, AVX2 and AVX512 detection with MSVC (#82554)
* Fixed NCCL detection issues of the Gloo library (#82773)
* Fixed objcopy version detection in NCCL cmake process (#82774)
* Fixed build error by changing COLORIZE_OUTPUT option to USE_COLORIZE_OUTPUT in cmake file (#83716)
* Set default value for NCCL make to MAX_JOBS if ProcessorCount returns 0 (#84231)
* Fixed intermittent link errors in NCCL build (#84245)
* Deleted `torch._dl` extension (#84361)
* Used unified source file list for BUCK build (#84770)

## Complex

* Fixed the derivative of `torch.acosh` for complex numbers (#80841).
* Removed unused conjugate kernels for real dtypes (2.2MB reduction in CUDA binary size) (#80374).

## torch.nn

* Fixed `nn.Embedding` ‘s `max_norm` argument when forward mode AD is used (#78560)
* Fixed `nn.ChannelShuffle` when given empty Tensors (#77029)
* Fixed `nn.RReLU` backward on CUDA (#80434)
* Fixed spurious warnings in `torch.nn.parallel.*` APIs (#81476)
* Fixed `nn.Conv2d` fallback implementation for single channel inputs and channels last weight (#82392)
* Fixed segfault in adaptive pooling for specific index values (#84010)
* Fixed type annotation in `nn.Conv{1,2,3}d` for in_channels (#84302)
* Fixed `nn.GeLU` for empty inputs (#84926)
* Fixed correctness issues for `nn.Conv2d` on ARM-based machines (#85711)
* Fixed `nn.ParameterList` printing of Tensors on the “meta” device (#78529)
* Fixed channels-first behavior for `nn.MaxPool3D` on CUDA (#80748)
* Fixed input shape validation `nn.MaxPool1d` (#85594)
* Fixed `nn.Softmax` for large input tensors (#84182)
* Fixed lower and upper bound checks for `nn.RReLU` (#84996)
* Fixed edge cases in `torch.nn.grad` by calling into the c++ backward kernel directly (#81839)
* Fixed `torch.nn.PixelShuffle` for empty inputs (#86262)
* Fixed consistency of output and input dtypes for `torch.nn.BatchNorm` (#84410)

## torch.optim

* Fixed `optim.SGD` `maximize` flag when `momentum` is involved (#81859)
* Fixed temporary bug where checkpoints from optimizers created with older PyTorch version could not be loaded (#83588)
* Fixed memory leak in `optim.lr_scheduler.CyclicLR` (#85462)
* Fixed initialization of `lr` in `optim.lr_scheduler.SequentialLR`  (#72856)

## BetterTransformer

* Cleaned up native transformer implementation (#78265)
* Added fastpath test for mask check flag (#82999)
* Added check for contiguous well-formed mask (#79927)
* Introduced mask contiguity check function (#79186)
* Fixed issue in softmax.cu with transformer error when mask `seqlen > 1024`  (#83639)
* Disabled Transformer/MHA fast path when autocast is enabled (#84722)
* Moved odd `num_head` in TransformerEncoder to `slow_path` (#83483)

## Composability

* Fixed `__torch_function__` bug in getindex that causes an error not set exception (#78781)
* Fixed `__torch_dispatch__` usage with inplace views (#79902)

## Dataloader

* Fixed `NoneType` object has no attribute `python_exit_status` when `DataLoader` exits (#83985)

## Functorch

* `functorch.grad`: fixed silent correctness issue from calling a view operation on a captured tensor followed by an in-place operation (#85374)
* `functorch.jacrev`, `functorch.jacfwd`: fixed loud in-place errors when passing in inputs to the transforms and mutating them (#84914, #84915)
* `functorch.vmap`: Fixed support for in-place view operations (`Tensor.unsqueeze_`, `Tensor.transpose_`, `Tensor.t_`, `Tensor.squeeze_`) (#82899, #82903, #82972)
* `functorch.vmap`: added an error on incorrect `weight` shape to `torch.nn.functional.prelu` (#83106)
* `functorch.vmap`: fixed support for multinomial (#83838)
* `functorch.vmap`: fixed incorrect support for `conv_transpose` with `groups > 1` (#84938)
* Fixed `vmap` x `vjp` x `vjp` composition for `torch.nn.functional.prelu` (#84939)
* Fixed printing tensors that are not being transformed over inside functorch transforms (#85556)
* Disallowed saved tensor hooks in functorch transforms to avoid silently incorrect behavior(#85972)
* Fixed `cross` to match unbatched behavior (#86926)

## LinAlg

* Strengthen the preconditions of `linalg.cross` (_#83798_)
* Fix memory issues in `linalg.lstsq` (_#85357_)
* Fix `linalg.lu_solve`/`torch.unpack` to prevent bad memory usage on CPU (_#85922_)
* Preserve the dim of the input in `matrix_exp`. (_#81330_)

## Sparse

* Fixed COO Tensors with less than two non-zero elements to always be marked coalesced. (#82426, #82085)
* Fixed CUDA kernel launch misconfiguration for `mul` on tiny COO tensors (#80254)
* Fixed silent type promotion bug by `select` if given all zero integer COO tensors(#82215)
* Fixed CUDA kernel coverage on 0-sized dense inputs for `torch.sparse.sampled_addmm` (#85194)

## torch.fx

* Fixed bug where curly brackets were not properly escaped in FxGraphDrawer (#83604)
* Fixed torch.fx.wrap to use the callable `function.__name__` rather than `function.__code__.co_name` (#84373)
* Added strictness check and made tensors into leaves if input tensors were leaves (#77474)
* Used getattr_recursive instead of getattr when splitting (#80011)
* Stopped ProxyTensor from turning aten::lift tensors into proxy objects (#81024)
* Fixed named_modules to be subscriptable (#81258)
* Fixed `to_folder` by adding custom_builtins to dump (#81433)
* Correctly unpacked constants when used in multi-return output (#82568)
* Replaced module name for torch.ops (#82395)
* Removed unnecessary `import warnings` (#82760)
* Don't constant propagate through nondeterministic functions (#83650)
* Don't extract tensor metadata from sparse tensors (#83669)
* Skipped folding side-effectful functions (#84016)
* Fixed make_fx issue by introducing get_attr into symbolic tracing (#84011)
* Disabled autocast cache during aotdispatch (#84035)
* Modified split_by_tags to retain output order (#84136)
* Made NormalizeArgs preserve node type (#85637)
* Fixed PyTree unpacking carrying forward type annotations (#81906)

## JIT

* Fixed conv-batchnorm folding for previously-broken datatype inputs during JIT freezing (#78241)
* Fixed lightweight dispatch OOM error by introducing selective build (#79215)
* Used signed integers in `CalculatedNecessaryArgs` to avoid underflow with schemas where all args have defaults. (#79331)
* Fixed indexing into a tensor with a tuple (#79335)
* Propagate `map_location` arg to `torch.jit.load` in `torch.load` (#78733)
* Improved JIT autodiff heuristics for determining whether outputs require gradients (#78392, #79498)
* Used streams for `import_ir_module` for pickle case to reduce memory usage (#80131)
* Added scripting support for "start" kwarg in `enumerate()`  (#80585)
* Turned off arc in CoreML backend, because throwing exceptions in arc code leaks memory (#79928)
* Suppressed virtual-dtor check on llvm_jit to fix NNC build (#81449)
* Fixed annotation extraction for python 3.10 (#81334) (#81334, #81506)
* Fixed `std::out_of_range` when using NNC and `ConstantChunk` input shapes are unknown (#82698)
* Limits constant chunk propagation for pw-node-only in NVFuser (#83083)
* When encountering dynamic types, one should cast it recursively. (#83218)
* Fixed handling of empty dim list in `sum_mean_dim` symbolic shape fn (#83357)
* Check existence of the array ref when tracing `resize_` to avoid `_MapBase::at runtime` error (#81422)
* Fixed `define_constant` pybind signature to match `std::complex` scalar in NVFuser (#83684)
* Cast to signed char to fix aarch64 build (#84429)
* Support `torch.ScriptObject` in `torch::jit::as_object` (#84398)
* NVFuser torchbench patch to take nvprim fallback when no cuda tensors are provided as inputs (#84411)
* Fixed coreml gpu flag not set (#84725)
* Print the real type for function schema arguments (#85103)
* Fixed `torch.jit.trace` check that was causing tracing to fail for MPS inputs (#84850)
* Throw an error instead of segfaulting when passing `None` to futures (#85304)
* Cherry pick sorting patch for NVFuser fusion segmented (#85620)
* Support freezing modules that don't have a forward method (#85779)

## Quantization

* Added channel axis bound checking in `fused_moving_avg_obs_fake_quant_*` (#78148)
* Disable use of qnnpack with `ceil_mode` of the `avgpool` op (#79028)
* Improve subpackage import in `torch.nn.quantized` (#84141)
* Fix segmentation fault in `QTensor.choose_qparams_optimized` (#85552)
* Enhance the `_rebuild_qtensor` function to support other device type other than CPU (#78234)
* Fix `at::from_blob_quantized_per_tensor_affine` strides calculation (#79314)
* Fix embedding quantization issue when memory format is not `contiguous` (#82605)
* Fix dispatch declaration bug about quantized op (#83649)
* Moved the order of x86 engine to avoid changing the default qengine (#86631)

## ONNX

* Fixed `aten::mul` with Boolean inputs (#81671)
* Fixed `add` and `sub` for non-tensor inputs (#81736)
* Fixed `RReLU` eval mode behavior (#82678)
* Fixed onnx optional node type in for/if block (#83599)
* Fixed `Interpolate`: use `half_pixel` instead of `pytorch_half_pixel`. (#80003)
* Fixed `argmin` and `argmax` edge case consistency with PyTorch. (#79503)
* Shape Type Inference and Propagation
* Fixed shape inconsistency when exporting scalar `log2` (#78701)
* Fixed inconsistent `rand` dtype (#79193)
* Fixed linalg `norm` output's shapes and dtypes (#79506)
* Fixed `any` and `all` outputs' shape (#79371)
* Fixed `prelu` output's shape (#79846)
* Fixed onnx logical functions' dtype (#79339)
* Fixed `hardshrink` and `softshrink` output's shape (#79695)
* Fixed quantization outputs' dtype (#79690)
* Fixed reduce node shape inference (#85765)
* Fixed bug using `std::copy_if` (#80999)
* Fixed default function value in `_optimize_graph` (#83996)
* Fixed constant folding unexpectedly adding folded constant as initializer (#79552)
* Fixed autograd subgraph recording with nested graphs (#82852)
* Disabled autocast cache in exporter (#84219)
* Removed static None graph output (#82623)
* Fixed float point detection for optional tensor (with unknown rank) within a list (#81386)
* Support `device().type()` string comparison with constant (#86168)
* Fixed `scalar_type_analysis` metadata for copied constant (#86716)
* Fixed triu/tril export with diagonal input (#86843)
* Ignore `print(Tensor)` during tracing (#86223)
* Updated training state logic to support ScriptedModule (#86745)

## AMD

* Fixed memory cross-border access on the ROCM platform (#76100)
* Set nvfuser default to disabled (#86369)

## CUDA

* Fix how we handle host memory in CUDA `getDeviceFromPtr` (#76902)
* Only sync CUDA if the operation is run on GPU (#80328)
* Do not use `thrust::lower_bound` on device (#80746)
* Fix `set_requires_cuda_init` (#81183)
* Fix behaviour of index_add / atomicAdd(bool,bool) (#85100)
* Fix IMA for topk (#83042)
* Use `opmath_t` for activation functions in Activation.cu (#77949)
* Fixed the invalid configuration argument error when running layer norm backward (#80893)
* Support non-standard bools in CUDA unique (#79392)
* Accept non-standard bools in more CUDA kernels (#78957)
* Fix cuda-mode and add more tests (#81898)
* Clear autocast amp cache in CUDA Graphs (#81896)
* Properly compute `batch_element_count` in `warp_softmax`  (#82927)
* Disabled autocast cache in torch.cuda.make_graphed_callables (#84289)
* Store RNG seed for CUDA graphs (#84967)
* Assert `lambda >= 0` in poisson distribution cuda kernel (#85906)
* Work-around 32-bit indexing failures in cuDNN batchnorm (#87861)
* Fixed 3d convolution_add_relu in V8 (#85055)

## Intel

* Fixed bug for thnn_conv2d when input's C is 1 and weight is channels last (#82392)
* Fixed oneDNN channels_last path issue (#83653)
* Fixed torch.config can't respect USE_MKLDNN flag issue (#75001)
* Made the data types of output and input consistent for batchnorm (#86784)
* Fixed the issue that cat result would be incorrect for channels-last (#85076)
* Fixed the performance issue that the for-loop before ExternallCall could not be parallelized (#85056)
* Fixed the performance issue that the for-loop before ExternallCall (#86516)

## MPS

* Fixed MPS operator torch.full for boolean types (#82575)
* Extend MPS Unary operators for empty tensors which should be a no-op (#82650)
* Fixed MPS operator `torch.scatter` for boolean types (#82685)
* Fixed MPS operator `torch.cat` for boolean inputs (#81480)
* Fixed typo in MPS allocator (#83465)
* Fixed MPS operator torch.full to handle uint8 types (#83697)
* Fixed creation of `MPS::Placeholder` behavior for transposed view operations (#85689)
* Fixed handling of output shape for empty inputs to binary ops in MPS backend (#85836)
* Added support for handling scalar inputs to MPS operations of `torch.scatter` and `torch.gather` (#85842)
* Support for handling compatible inputs to MPS operation of torch.where (#85946)
* Added support for inputs with datatypes Short, Byte & Char to torch.dot MPS operation by casting to int32 when needed (#86140)
* Remove incorrect asserts in MPS backend from Copy.mm file (#86184)
* Added support for handling of 1D inputs for MPS operation `torch.nll_loss` (#81290)
* Get correct size of the view tensor when copying from cpu to mps device (#81730)
* Fix issues exposed in MPS testConsistency tests. The fix includes correct handling of types in smooth l1 loss, 0 dimensions for torch.repeat and empty inputs for torch.cat operations (#81735)
* Handle Integer inputs for MPS linear layer by returning error of unsupported data types (#82183)
* Workaround int8 datatype outputs in MPS for View operations (gather) by casting it to int8 (#82315)
* Improve handling of empty outputs and fix MPS linear layer’s handling of transposed Tensors in test consistency (#83124)
* Fixed handling of conv1D and conv2D MPS operations with non-matching strides/paddings (#83522)
* Fixed handling of MPS::Placeholder when View operation is missing gather graph (#83744)
* Fixed the index handling in MPS for torch.constant_pad_nd operations with single-dimension input (#83745)
* Handle casting for MPS torch.div operation in case of type mismatch (#84742)
* Fix device (MPS) to host (cpu) copy by casting from a smaller dtype to a bigger dtype (#84928)
* Ensure as_strided_tensorimpl is never called with MPS (#85020)
* Fixed integer rounding crash in torch.div MPS operation on M1 (#85016)
* Fixed crash in MPS bitwise ops on Mac x86 platforms. (#85285)
* Fixed crash in MPS Conv1d backward operation for NHWC (#85283)
* Added support for MPS reduction operations of scalar edge-cases (#83743)
* Fixed memory corruption in torch.var operation for MPS (#85571)
* Fixed memory leaks in MPS that cause the MTLBuffers not to be released and cause OOM (#85661)
* Fix test consistency error in MPS due to type mismatch between int8 and uint8 types (#85666)
* Fixed shape issues for torch.clamp op in MPS (#85673)
* Fixed handling of TensorBase shapes for view ops in MPS for case of multiple slices on a Tensor (#85934)
* Fix the dimension of padding to match the input's dimension for MPS Pad operations (#85990)
* Fix non-contiguous to contiguous copy of MPS tensors (#86056)
* Remove `std::cout` from MPS `multinomial` operation (#86246)
* Do not dispatch empty job in bitwise_not (#87286)
* Made copy from CPU always add storageOffset (#86958)
* Revamped `copy_to_mps_` implementation (#86956)

## Package

* Added fix for implicit numpy dependency (#78979)
* Allowed torch._C to be recognized a module in torch.package (#80917)
* Ignore return value of function declared with 'warn_unused_result' for torch::deploy (#84862)
* Removed torch::deploy from pytorch (#85953)

## Profiler

* Fixed build failure in python 3.10 (#81812)
* Pop `KinetoThreadLocalState` at the start of post processing. (#77996)
* Fixed record function inputs_valid_ check (#78002)
* Weakened ordering check during post processing. (#78563)
* Fixed Python parent id (#79356)
* GIL acquire needed in ValueCache::trimPrefixes (#81061)
* Added ephemeral inputs to the value cache. (#81958)
* Fixed profiling with record_shapes=True and nested tensor (#82854)
* Proper reset execution graph data in remove callback registration (#82910)
* Solved two syntax issues when dumping execution graph result to json file. (#81854)
* Set end time on python events when profiling stops. (#83621)
* Don't try to collect strides for non-strided tensors (#83935)
* Add null handling to `AppendOnlyList::copy` memcpy path. (#83963)
* Add quoted metadata API to remove empty trace cpu_op metadata (#84128)
* Make `RecordQueue` manage the lifetime of `PythonTracer`. (#83964)
* Don't assign in AppendOnlyList::emplace_back (#85716)
* Fixed traversal utility (#85717)
* Fixed python object reference counting (#85847)

## Visualization

* Removed dependency on `torch.onnx` in `graph` (#82628)
* Updated `Image.ANTIALIAS` to `Image.Resampling.LANCZOS` in summary (#85679)

## Vulkan

* Fixed the `aten::cat` operator registration (#78806)
* Fixed a bug in GRU where incorrect behaviour was being observed when `H_in != H_out` (#78945)
* FIxed a possibly null pointer dereference in the `aten::mm` operator when using passing an empty bias (#79701)
* Code under `ATen/native/vulkan/api` was essentially rewritten (more details below) and as a result of these refactors, it is now possible to concurrently execute multiple Vulkan models due to correct synchronization when recording to a Vulkan command buffer (#80959)

## Mobile

* Moved saving storage to the last step. (#78024)
* Fixed build For Model Tracer (#84755)
* Skip TestNNAPI tests if QNNPACK is not supported (#82882)
* Extended LinearPackedParamsBase **getstate**/**setstate** deadline in `check_forward_backward_compatibility.py` Allowlist (#81135)
* Removed LinearPackedParamsBase **getstate**/**setstate** from `check_forward_backward_compatibility.py` Allowlist (#81048)
* Fixed `ao::sparse::BCSR` missing in qlinear serialize and deserialize when USE_FBGEMM and USE_PYTORCH_QNNPACK are not set (#81256)
* Updated `model_ops.yaml` (#82444)
* Fixed signed/unsigned compare for Metal (#86068)
* Re-added benchmarking files to ios TestApp (#85539)

## Distributed

#### `Distributed(c10d)`

* Ensured tensors are contiguous for autograd enabled `all_gather`. (#79747)
* Fixed data race condition of `batch_isend_irecv` (#82450)
* Fixed `distributed_test.py` flakiness by turning off async_errror_handling (#78797)
* Reenabled `isinstance` with `torch.distributed.ReduceOp` (#87303)

#### `DistributedDataParallel`

* Enabled `AllReduceCommHook` to accept `instrusive_ptr` (#80975)

#### `FullyShardedDataParallel`

* Fixed `full_optim_state_dict()` hang (#80712)
* Fixed exec order validation for ignored modules across ranks (#79533)
* Cleaned prefixes when searching for params / buffers to ignore (#78278)
* Returned original module when fsdp wrapped model call .module (#78671)
* Fixed a small bug of pre_backward_hook params prefetch (#78851)
* Fixed param name prefixes for ignored modules (#79955)
* Fixed FSDP when not all outputs get gradient in backward (#80245)
* Fixed that MP config not being passed to FSDP (#80869)
* Fixed FSDP device_id when CPU offloading (#82892)
* Fixed FSDP not all outputs used in loss (#83195)
* Fixed the FQN not found issue for load sharded_state_dict when using activation checkpoint (#84253)
* Fixed `pin_memory()` for CPU offloading (#85048)
* Fixed memory regression! (#85087)
* Implemented a short-term fix to remove `optim_input` (#84201)

#### `torch.distributed.elastic`

* Ensured that exit code is propagated from Child to parent process (#81408)

#### `torch.distributed.rpc`

* Only initialize CUDA if there are devices specified in `init_rpc` (#80180)
* Fixed the wrong usage of `RRefContext::handleException` by having a new API `RRefContext::handleExceptionSilent` (#83166)
* Changed to avoid initializing storage for empty Optionals (#78947)

## Infra (RelEng)

* Made bazel changes to make “bazel query ...” work (#78870)
* Fixed C API to be compatible with latest Python 3.11 beta (Please note that 3.11 binaries are not fully functional)  (#81242)

# Performance

## Python API

* Fixed use of temporary buffers for tensors in `torch.save`. (#80404)
* Fixed and improved the efficiency of the backward for `torch.xlog{*}` functions. (#82713)
* Vectorized `.copy()` acting between different dtypes on CPU (#80905)
* Vectorized `bfloat16` conversions on CPU (#80906)

## Autograd

* Codegened autograd nodes no longer is smarter about which gradients to compute (#82544)
* Made the derivative of masked_fill more efficient (#83515)
* `torch.where` no longer materializes a zero-filled tensor in its backward (#83043)

## torch.nn

* Speed up `nn.Module` constructor by not calling custom `setattr` (#77098)
* Speed up CPU `nn.BatchNorm` implementation by using `torch.zeros()` directly (#82558)
* Speed up `nn.Module.load_state_dict` (#85743)

## BetterTransformer

* Added nn.module activation support in BetterTransformer (#78394), in addition to functional support which is not available in Torchscript
* Added mask identifier for multiplexed src_mask/src_key_padding_mask in BT (#81947)
* Added a small fastpath test for native multi-head attention (#81432)

## Composability

* Release GIL when doing shared memory copies on Tensors (#85389)
* Some micro-optimizations in `RecordFunction`, the core util used by the profiler (#76266)
* `c10::detail::ReplaceAll`: avoid some unnecessary allocations (#79915)

## Dataloader

* Moved loop content into a function to ensure we don't preserve `Tensor` in `pin_memory` thread (#83595)

## LinAlg

* Simplified and optimized `linalg.solve` (_#74046_)
* Improved heuristics for `linalg.lu_solve` when B is a matrix (_#79838_)
* Small optimization of `linalg.cholesky` (_#81316_)
* Prefer contiguous output from mkldnn_bf16_gemm (_#82968_)
* CPUBlas: Use mkldnn optimized BFloat16 matmul for gemm (_#65840_)
* Updated and improved the heuristics for `linalg.lu_solve` (_#73878_)
* Optimized `linalg.householder_product` backward to be more memory-efficient (_#84627_)

## Sparse

* Improved `to_sparse_bsr` for batched dense inputs (#83085)
* Improved `to_dense` for CSC (#79635)
* Improved `index_select` performance for COO input on CUDA (#77551)
* Improved `mul(COO, COO)` performance with broadcasting in dense dims. (#83428, #85336)

## JIT

* Improved coreml load time by loading cpu model first, while asynchronously loading a model (#80941)
* Improved `torch::jit::as_{module,object}` performance (#84399)
* Replaced `IValue::toString()->string()` with `IValue::toStringRef()` (#85437)

## Quantization

* Allow contiguous inputs run into `qcat_nhwc_stub` when dim is last dimension (#72575)
* Enable qlinear dynamic parallelization with fbgemm (#84033)

## CUDA

* Fixed perf regression introduced in #70943 (#78588)
* Improved small sort performance on CUDA (#79627)
* Use cub::BlockRadixSort to improve medium length sort performance (#79628)
* Use cub::BlockRadixSort to improve medium length sort performance (#79628)
* Increased size limit on calling CublasLt in addmm by 32x (#82922)
* Don't synchronize single element any/all reductions (#84465)
* Added col2im_batched kernel (#84543)
* Exposed fast get_current_stream (#78165)
* Pool cudaEvents in CUDACachingAllocator (#78279)

## Intel

* Optimize the copy of BFloat16 to Float and Float to BFloat16 (_#79685_)
* Improve performance of ONEDNN backend (_#84470_)
* Optimize softmax backward and logsoftmax backward _#80114_
* Improve sort multi-core perf by adjusting grain_size w.r.t. dim_size (_#74897_)
* Add fast path of `qmean`/`qstd` for quantized CPU (_#80579_)
* Use direct memcpy in `qcat` when all the inputs and output share the same scale and zero_point (_#71903_)
* Vectorize scalar remainder in quantized kernel for normalization (_#79673_)
* Enhance add_out_dense_sparse_cpu for hybrid sparse tensor (_#23057_)

## MPS

* Performance improvements for the MPS backend by changing commitAndWait to commit & fixing high memory consumption for View operations. Also improved scalar handling in MPS Allocator (_#81951_)
* Improved performance for MPS backend by reducing the number of command buffers created and hence CPU overhead. It uses commitAndContinue feature in MPS (_#81338_)
* Added direct MPS implementation for constant_pad_nd operation which improved performance as the generic implementation was heavily reliant on View ops which are slow (_#82366_)
* Removed checks that incur unnecessary syncs for MPS device with tensor.item() (_#82505_)
* Enabled Graph caching in MPS for torch random ops with Philox engine (_#85833_)
* Added specialized memory pool for scalar values in MPS which improved performance in torchbench networks (_#85817_)
* Improved memory usage and performance by utilizing garbage collector and adaptive commit feature in MPS (_#86119_)

## Profiler

* Optimize getStepCallbacks for common case of no active callbacks for kineto (#77804)
* Use custom AppendOnlyList for op_events to reduce the number of atomic operations (#78643)

## Vulkan

* When waiting on the result of a `VkFence`, busy polling is now used instead of a single call to `VkWaitForFences` with no timeout. This can improve benchmark performance by up to 50% by ensuring that the CPU stays at a high frequency when waiting for work on the GPU to complete (#81470)

## Mobile

* Added compilation_preference & relax_f32_to_f16 APIs (#78758)
* Made flatbuffer loads faster if loading as mobile module. (#78998)
* Stream pkl (#79931)
* Used Apple's Accelerate framework for blas acceleration (#80449)
* Read via FileAdapter when loading files in torch if not flatbuffer for lite_interpreter (#84028, #84296)

# Documentation

## Python API

* Fixed `torch.as_array` documentation formatting (#78485)
* Fixed default value for `storage_offset` in `torch.as_strided` documentation (#78202)
* Removed warning in documentation that `torch.real` is only supported on complex types (#78644)
* Improved reproducibility documentation for the random number generator and `torch.use_deterministic_algorithms` (#78849)
* Fixed example in documentation for serialization (#79454)
* Fixed `torch.linspace` documentation for dtype (#81371)
* Fixed typo in documentation for `torch.distributions.Dirichlet` (#82062)
* Fixed example  in `torch.dist` documentation (#82104)
* Updated `torch.narrow` documentation to reflect that `start` can be a Tensor (#85180)
* Added documentation for `pin_memory` and `layout` arguments to `torch.new_{zeros, ones, full}` (#85605)
* Added documentation for `pin_memory` argument to `torch.{rand, randn}` (#85219),  (#85221)
* Added argument default values to documentation for `torch.rot90` (#85610)
* Removed `out` argument from documentation for `torch.squeeze` (#85222)
* Fixed `torch.log` example (#78776)
* Fixed `torch.argmin` docs for `keepdim` argument (#78888)
* Updated examples in documentation for `torch.use_deterministic_algorithms` (#82003)
* Changed docstring type `callable` to `Callable` for consistency (#82487)
* Added documentation for `torch.narrow_copy` (#84493)
* Improved documentation for `torch.signbit` (#78349)
* Added doc string for `torch.library.Library.impl` (#81047)
* Renamed `_Typed/_UntypedStorage` to `Typed/UntypedStorage` and updated documentation for `torch.storage` (#82438)
* Added documentation for `torch.unflatten()` (#81399)

## Autograd

* Improved autograd custom function docs (#81340)
* Added randomness case to the autograd notes (#78617)

## Complex

* Added a note on CUDA 11.6 (#80363)

## torch.nn

* Fixed docstring and image for `nn.LeakyReLU`  (#78508, #79102), `nn.ELU` (#78909), `nn.GRU` (#79380), `nn.Hardswish` (#70993), `nn.GeLU` (#85790)
* Fixed docstring for `nn.CrossEntropyLoss` (#79568 and #82538), `nn.MultiMarginLoss` (#84513)
* Fixed high level `nn.init` module doc to reflect that all functions run with `torch.no_grad` (#80882)
* Fixed docstring for `nn.Module.state_dict` (#83104)
* Updated docstring for `scale_factor` in `nn.functional.interpolate` (#80807)

## torch.optim

* Fixed docstring for `optim.lr_scheduler.ChainedScheduler` (#79775)
* Fixed docstring for `optim.swa_utils.SWALR` (#79836)

## Composability

* Fix `MetadataTensor` example in `__torch_function__` docs (#78073, #78707)

## Functorch

* Fixed the model description in the functorch ensembling notebook (#83603)
* Fixed indentation in functorch limitations docs (#85346)
* Updated functorch installation instructions (#85854)
* Fixed functorch whirlwind tour notebook to be runnable (#85974)
* Documented new installation instructions for functorch (#86823)

## LinAlg

* Improve `torch.lu_unpack` docs (#77635)
* Fix inconsistent default `rcond` value (#82887)

## Sparse

* Updated `scatter_add_` documentation to fix argument name (#80223)
* Updated `torch.sparse` docs to better cover CSR/CSC/BSR/BSC (#82108)
* Added torch.sparse overview section (#85265)
* Updated documentation for `mm` family ops and `F.linear` to note limited sparse support (#86220)

## torch.fx

* Fixed decomposition example (#79807)
* Added `__all__` to various submodules in torch.fx, distributions, distributed, package (#80367)
* Added warning about DCE in FX being unsound with mutation (#81818)

## Quantization

* Replace `qconfig_dict` with `QConfigMapping` in docs (#78533)
* Corrects typo in quantization docs (#81687)
* Additonal fixes for `quantize_fx` docs (#84587)
* Add example for the error message for fixed qparam ops (#84666)
* Add types for scale and zero_point tensor for `torch.fake_quantize_per_channel_affine` docs (#85733)
* Updated quantization docs to show per channel support for `conv1d` (#81349)
* Add `torch.ao.nn.quantizeable` modules documentation (#79957)
* Add more detailed docs for `torch.ao.quantization.quantize_fx.{prepare_fx|prepare_qat_fx|convert_fx}` (#83132)

## ONNX

* Added a table of unsupported aten operators in the documentation (#84496)

## CUDA

* Fixed jiterator doc format (#78471)
* Use generic amp autocast in example and specified dtype (#79579)
* Fixed small typo in cuda.rst (#84012)
* Added user facing documentation for CSAN (#84689)
* Fixed broken docstring for `set_float32_matmul_precision` (#78949)

## MPS

* Update Persons Of Interest file for MPS (_#81757_)
* Update backends.rst for MPS (_#82525_)

## Package

* PackageExporter does not have file_structure (#79948)
* Updated package.rst to not include hermetic claim (#81019)
* Fixed typos in `torch.package` documentation (#82994)
* Fixed typo in torch/package/_mock.py (#84508)

## Distributed

#### `Distributed(c10d)`

* Fixed some links in torch/distributed/CONTRIBUTING.md  (#79855)
* Updated dist.scatter() documentation (#86069)
* Fixed docstring of `scatter_object_list` (#84596)
* Fixed doc string in `reduce_scatter` (#84983)

#### `DistributedDataParallel`

* Corrected the DDP wrap example by removing pg in DDP wrap (#83034)

#### `FullyShardedDataParallel`

* Improved auto wrap policy doc (#78400)
* Corrected comments in FSDP for gradient averaging (#80456)
* Updated `ShardingStrategy` and `_free_full_params()` docs (#80894)
* Added mentioning of `optim_input` to be removed after 1.13 in the BC breakage warning (#85963)

#### `torch.distributed.rpc`

* Updated distributed/CONTRIBUTING.md to remove ProcessGroupAgent references and add test instructions (#78625)

## Infra (RelEng)

* Added some documentation about the stats uploading process for CI (#79504)
* Fixed release doc builds (#79865)
* Updated release.md with release candidate validation steps (#79889)

# Developers

## Autograd

* Added the ability to register a hook to grad_fn with `.register_prehook`(#83226)

## Build

* Modified nccl_dependency to take dev mode (#79169)
* Moved pytorch buck targets to shared build (#79330)
* Added kineto and flatbuffers to OSS BUCK (#79860)
* Updated llvm deps for Buck build (#79919)
* Moved aten targets to shared buck file (#79966)
* Updated buck_setup.sh (#80467)
* Minor fix for shared build (#80739)
* Deleted CCACHE_DISABLE and SCCACHE_DISABLE from nccl.cmake file (#84007)

## Composability

* `TorchDispatchMode` and `TorchFunctionMode` extension points have been added. They are similar to their `__torch_function__` and `__torch_dispatch__` counterparts, but can be used as context managers that intercept **all** torch operator calls, including factory functions. These API’s are still experimental and aren’t quite user facing yet, and we will add more documentation as they are hardened. See [this post](https://dev-discuss.pytorch.org/t/what-and-why-is-torch-dispatch/557) for more details.   (#78214, #78822, #78847, #84774, #83925, #79143, #77667, #80992, #80995, #80998, #82647, #83372)
* A large amount of hardening to `FakeTensor` and `FakeTensorMode`, a `__torch_dispatch__` style mode that allows you to run shape/dtype/device inference. This is similar to the “meta” device, but fake tensors also faithfully store device metadata, and the logic lives in python. (#77969, #77972, #77971, #78516, #78090, #78836, #78895, #78536, #78677, #78522, #78523, #78972, #79170, #80115, #80193, #80544, #81739, #82281, #82574, #82066, #82449, #82337, #82571, #82593, #82172, #84387, #85065, #82846, #85658, #85759, #85920)
* Added some new tags and beefed up tags support for operators in the dispatcher:
    * Add data_dependent_output tag (#83312)
    * Add nondeterministic tags in tags.yaml and add the nondeterministic_seeded tag to all functions in native_functions.yaml defined as nondeterministic by alias_analysis.cpp (#81440)
    * Allow specifying operator tags when registering an operator to the dispatcher (#79322)
    * add `inplace_view` tag to `resize_()` (#82667)
* Make string serialization of C++ FunctionSchema consistent with torchgen.model.FunctionSchema (#77926)
* Added support for custom namespaces in `torchgen` (#78015, #79733, #81362, #81581)
* Generate kernels for codegen’d `out=` operators (#78626, #81437)
* Added a new alias dispatch key for functional to view op decompositions (#79615)
* Added an env var for dispatcher debug logging (#81846, #82277)
* Fixed printing of DispatchKey in operator not found message (#81637)
* Added test that all BackendComponents are covered by toString (#81713)
* Refactored functionality and backend keys to reduce duplication (#81752)
* Made factory functions `CompositeExplicitAutograd`, so they show up as primitives in `__torch_dispatch__` (#82470)
* Added an `OpOverload.decompose()` API, for running an operator’s decomposition if one exists (#83075)
* Fixed our dispatcher schema parser when parsing tensor list alias annotations (#84005)
* Allowed subclasses of `c10::TensorImpl()` to override non-virtual tensor methods (#84806)
* Made pytorch headers consumable from c++20 code bases (#79985)
* Added meta device support to `_UntypedStorage` and `_TypedStorage` (#78008)

## torch.fx

* Added debug statements for small ACC subgraphs elimination (#80117)
* Checked node type before fetching users (#80166)
* Detected ProxyTensor layering violations (#80994)
* Increased stack level for get_attr warning (#81041)
* Preserved a node’s stack trace (#82670, #83050, #83558, #83706, #83960)
* For quantization, removed `WEIGHT_INDEX_DICT` and `BIAS_INDEX_DICT` and replaced with `node_arg_is_weight` and `node_arg_is_bias` (#83263, #83848)
* Asserted that ProxyTensorMode does not accidentally bake in constants (#83297)
* Improvements to FX Minimizer (#83833)
* Ported matmul compositeimplicitautograd impl into core (#85239)
* OpInfo for Slice (#85554)
* Raised errors in fx.Interpreter with Node info (#85810)

## Quantization

* Enabled support for quantized fill of nhwc tensors (#79025)
* Tests for code snippets in quantization docs (#79923)
* Eliminate Named tensor warnings in XNNPACK and QNNPACK (#77762)
* Added earlier termination and improved error message for calling `min` and `max` ops on per channel quantized tensors. (#79036)
* Added warnings to quantized dynamic conv and linear ops when `reduce_range=true` (#79273)
* Add assertions to fix `torch::jit::load bugs` (#79192)
* Optionally clamp weights post quantization (#83438)

## ONNX

* `onnx.verification` Tool to verify exported model discrepancy between sets of inputs (#78323)
* Symbolic function registration is now done via decorators (#84709)
* `g.op` methods now exposed via the GraphContext class (#84728)
* Initial version of diagnostics infrastructure. (#85107)
* Add dtype check in onnx verification (#79263)

## Intel

* Added native impl for group norm on quantized CPU for channels-last inputs: (_#70520_)
* Added `qscheme` check for quantization observer (_#80126_)
* Added oneDNN graph fuser context API and unittest (_#82491_)
* Added eltwise OPs for NNC: `mish` and `elu` (_#80586_)
* Support BF16ImmPtr (_#84041_)
* Enabled fusion of conv with elementwise OP for NNC (_#77157_)
* Channels last propagation within NNC fusion group (_#76948_)
* Lowering function generates the output buffer with the specified stride for NNC(_#76529_)
* Simplified IfThenElse and CompareSelect within for-loop for NNC (_#76793_)
* Do not pull in _autocast_* ops into NNC (_#85140_)

## MPS

* Improve MPS test by extending `test_no_warnings_on_input` by capturing any output (_#79163_)
* Add testcase in test_mps for circular mode in torch.pad (_#81455_)
* Fixed build warnings while building with MPS on Mac platforms (_#83048_)
* Add per-op MPS gradient tests and update skips for TestConsistency (_#84242_)

## Profiler

* New event representation in profiler (#77693, #77694, #77695, #78163, #79173, #81965, #80797, #81319, #81320, #81321, #81322, #80822, #82993)
* Build call tree for profiled events (#77698, #80810)
* Copy rollbear/strong_type to `c10/util` (#78162)
* Collect Layout and expose TensorMetadata (#81155)
* Added support for storing scalar values in profiling (#81843)
* Added support for Device (#82787)
* Added SOFT_ASSERT to gracefully recover from invariant violations (#82689)
* Added support for accessing strides and scalars (#80072)
* Record nn.Module's parameters (#83209)
* Extend Python bindings (#83622)
* Capture storage data pointer (#84276)
* Cleaned up Tensor representation (#85161)
* Compute unique IDs for Tensors (#85162)
* set_class util (part 1 of Record Optimizer) (#84779)
* Tracking Optimizer (part 2 of Record Optimizer) (#84920)
* Optimizer param_groups (part 3 of Record Optimizer) (#85784)
* Optimizer states (part 4 of Record Optimizer) (#85840)
* Extend ID assignment to allocations and frees (#85719)
* Made `name` a property. (#85720)
* Added dtype to `_TensorMetadata` (#85721)
* Updated python binding type annotations (#85722)
* Started moving python bindings out of autograd (#82584)

## Vulkan

* Vulkan operators that use prepacking have switched from using individual `OpContext` classes with `PackedContext` classes that inherit from a generic `VulkanOpContext` class which should reduce boilerplate code when implementing new ops that require prepacking (#78814, #78815, #78816, #78817, #78818, #82730, #83526)
* Code under `ATen/native/vulkan/api` was essentially rewritten to improve code organization and readability. The refactor implements RAII patterns for the classes used to represent Vulkan handles to facilitate proper resource management and re-designed how the `Context` class functions in order to enable concurrent execution of multiple Vulkan models. The stack of PRs containing these refactors can be found at #80699
* Lint is now enforced in the `ATen/native/vulkan` (#81390)
* The VulkanMemoryAllocator version used was upgraded to 3.0.1, which now lives under `third_party` (#81472, #83906, #83934)
* Shader layouts are now automatically generated based on the GLSL code (#81715, #81716)

## Distributed

#### `torch.distributed`

* Added **all** to torch.distributed and tensorboard submodules (#80444)
* Added **all** to torch.{fx, distributed, backends} submodules (#85079)
* Added **all** to fx, fistributed and cuda submodules (#85080)
* Added **all** to torch.distributed, futures, fx, nn, package, benchmark submodules (#80520)
* Added **all** to torch.distributed submodules (#80523)
* Eliminated code duplication in distributed rendezvous (#81577)
* Refactored distributed to use absolute header path (#85780)

#### `torch.distributed.elastic`

* Added **all** for torch.nn.modules, torch.distributed.elastic, torch.nn.utils submodules (#80240)
* Fixed macos public bindings failures (#80970)

#### `Distributed(c10d)`

* Logged full rank fingerprint mismatches in ProcessGroupWrapper (#79901)
* Added environment parse function that supports default value (#85563)
* Added host and port to TCPStore pyi definition (#84636)
* Added underlying_store property for PrefixStore (#84640)
* Enabled per-thread ProcessGroup for testing (#84153)
* Moved ProcessGroup::Work into a separate class (#83680)
* Install c10d headers with absolute path (#86257)

## Infra (RelEng)

* Migrated off xenial gcc5.4 from merge rules (#78137)
* Added functionality for rebasebot to rebase onto viable/strict branch (#78276)
* Pinned protobuf version to 3.20.1 in docker CI build (#78369)
* Removed gcc5.4 from docker/build.sh (#78405)
* Removed gcc5.4 jobs from CircleCI config (#78555)
* Added merge rules for “pytorch distributed” module (#78751)
* Added onnx / test to required merge rules (#78790)
* Added userbenchmark support to TorchBench CI (#78794)
* Installed torchdynamo as part of most CI jobs (#79051)
* Removed linux-xenial-py3_7-clang7-asan from merge rules (#79088)
* Ran torchdynamo tests on PyTorch Linux CI (#79099)
* Centralized commit pins in a folder (#79150)
* Moved CUDA flags out of --per_file_copts into the cu_library macro (#79414)
* Moved CI to cuda-11.6 (#79921)
* Enabled pytest to run test_ops, test_ops_gradients, test_ops_jit in non linux cuda environments (#79898)
* Upgraded pytorch nightly docker python version to 3.8 (#80051)
* Updated Dockerfile to install cmake as part of conda install (#80258)
* Re-enabled vulkan test (#81368)
* Enhanced mergebot with the feature of posting the PR Comment on cancel (#82744)
* Changed nccl build to be single-threaded (#83173)
* Added process for maintaining Build + CI contributors list (#83869)
* Implemented mechanisms to block land checks if the PR hasn't been approved yet (#84239)
* Allowed External Scripts (e.g. vscode) To Discover and Execute unittest Tests (#85584)
* Updated the pinned torchdynamo hash to `6ead5cae0d1234aa64db06fe230ef56e12ec76fe` (#85683)
* Updated the pinned torchvision hash to `d7d90f56117ce0955332846a5f90b8d1346c4c09` (#85776)
* Modified all functions (except factory functions) to support SymInt and update xla hash to `f2b36df6a1a80137eff7644e6d0f4eeb7ff429d6` (#86078)
# ===== RELEASE pytorch/pytorch v2.0.0 =====

# PyTorch 2.0 Release notes

- Highlights
- Backwards Incompatible Changes
- Deprecations
- New Features
- Improvements
- Bug fixes
- Performance
- Documentation

# Highlights

We are excited to announce the release of PyTorch® 2.0 ([release note](https://github.com/pytorch/pytorch/releases)) which we highlighted during the [PyTorch Conference](https://www.youtube.com/@PyTorch/playlists?view=50&sort=dd&shelf_id=2) on 12/2/22! PyTorch 2.0 offers the same eager-mode development and user experience, while fundamentally changing and supercharging how PyTorch operates at compiler level under the hood with faster performance and support for Dynamic Shapes and Distributed.

This next-generation release includes a Stable version of Accelerated Transformers (formerly called Better Transformers); Beta includes torch.compile as the main API for PyTorch 2.0, the scaled_dot_product_attention function as part of torch.nn.functional, the MPS backend, functorch APIs in the torch.func module; and other Beta/Prototype improvements across various inferences, performance and training optimization features on GPUs and CPUs. For a comprehensive introduction and technical overview of torch.compile, please visit the 2.0 [Get Started page](https://pytorch.org/get-started/pytorch-2.0).

Along with 2.0, we are also releasing a series of beta updates to the PyTorch domain libraries, including those that are in-tree, and separate libraries including TorchAudio, TorchVision, and TorchText. An update for TorchX is also being released as it moves to community supported mode. More details can be found in this [library blog](https://pytorch.org/blog/new-library-updates-in-pytorch-2.0/).

This release is composed of over 4,541 commits and 428 contributors since 1.13.1. We want to sincerely thank our dedicated community for your contributions. As always, we encourage you to try these out and report any issues as we improve 2.0 and the overall 2-series this year.

Summary:

- torch.compile is the main API for PyTorch 2.0, which wraps your model and returns a compiled model. It is a fully additive (and optional) feature and hence 2.0 is 100% backward compatible by definition.
- As an underpinning technology of torch.compile, TorchInductor with Nvidia and AMD GPUs will rely on OpenAI Triton deep learning compiler to generate performant code and hide low level hardware details. OpenAI Triton-generated kernels achieve performance that's on par with hand-written kernels and specialized cuda libraries such as cublas.
- Accelerated Transformers introduce high-performance support for training and inference using a custom kernel architecture for scaled dot product attention (SPDA). The API is integrated with torch.compile() and model developers may also use the [scaled dot product attention](https://pytorch.org/docs/2.0/generated/torch.nn.functional.scaled_dot_product_attention.html) kernels directly by calling the new scaled_dot_product_attention() operator.
- Metal Performance Shaders (MPS) backend provides GPU accelerated PyTorch training on Mac platforms with added support for Top 60 most used ops, bringing coverage to over 300 operators.
- Amazon AWS optimize the PyTorch CPU inference on AWS Graviton3 based [C7g instances](https://aws.amazon.com/blogs/aws/new-amazon-ec2-c7g-instances-powered-by-aws-graviton3-processors/). PyTorch 2.0 improves inference performance on Graviton compared to the previous releases, including improvements for Resnet50 and Bert.
- New prototype features and technologies across TensorParallel, DTensor, 2D parallel, TorchDynamo, AOTAutograd, PrimTorch and TorchInductor.

<table>
  <tr>
   <td>
<strong>Stable</strong>
   </td>
   <td><strong>Beta</strong>
   </td>
   <td><strong>Prototype</strong>
   </td>
   <td><strong>Platform Changes</strong>
   </td>
  </tr>
  <tr>
   <td>Accelerated PT 2 Transformers
   </td>
   <td>torch.compile
   </td>
   <td>DTensor
   </td>
   <td>CUDA support for 11.7 & 11.8 (deprecating CUDA 11.6)
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>PyTorch MPS Backend
   </td>
   <td>TensorParallel
   </td>
   <td>Python 3.8 (deprecating Python 3.7)
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>Scaled dot product attention
   </td>
   <td>2D Parallel
   </td>
   <td>AWS Graviton3
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>Functorch
   </td>
   <td rowspan="2" >Torch.compile (dynamic=True)
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>Dispatchable Collectives
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>torch.set_default_device and torch.device as context manager
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>X86 quantization backend
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>GNN inference and training performance
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>

\*To see a full list of public 2.0, 1.13 and 1.12 feature submissions click[ here](https://docs.google.com/spreadsheets/d/1H3jazwO8BBCwK8JwLNYspLiHfUrzshEtyqjL-X93I9g/edit#gid=790902532)

# Backwards Incompatible Changes

### **Drop support for Python versions <= 3.7 (#93155)**

Previously the minimum supported version of Python for PyTorch was 3.7. This PR updates the minimum version to require 3.8 in order to install PyTorch. See [Hardware / Software Support ](https://github.com/pytorch/pytorch/blob/893aa5df3f2a475c91ea8eadb1353812e52fb227/RELEASE.md#python) for more information.

### **Drop support for CUDA 10 (#89582)**

This PR updates the minimum CUDA version to 11.0. See the [getting-started](https://pytorch.org/get-started/locally/) for installation or [building from source](https://github.com/pytorch/pytorch#from-source) for more information.

### **Gradients are now set to `None` instead of zeros by default in `torch.optim.*.zero_grad()` and `torch.nn.Module.zero_grad()` (#92731)**

This changes the default behavior of `zero_grad()` to zero out the grads by setting them to `None` instead of zero tensors. In other words, the `set_to_none` kwarg is now `True` by default instead of `False`. Setting grads to `None` reduces peak memory usage and increases performance. This will break code that directly accesses data or does computation on the grads after calling `zero_grad()` as they will now be `None`. To revert to the old behavior, pass in `zero_grad(set_to_none=False)`.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
>>> import torch
>>> from torch import nn
>>> module = nn.Linear(2,22)
>>> i = torch.randn(2, 2, requires_grad=True)
>>> module(i).sum().backward()
>>> module.zero_grad()
>>> module.weight.grad == None
False
>>> module.weight.grad.data
tensor([[0., 0.],
        [0., 0.]])
>>> module.weight.grad + 1.0
tensor([[1., 1.],
        [1., 1.]])
```

</td>
<td>

```Python
>>> import torch
>>> from torch import nn
>>> module = nn.Linear(5, 5)
>>> i = torch.randn(2, 5, requires_grad=True)
>>> module(i).sum().backward()
>>> module.zero_grad()
>>> module.weight.grad == None
True
>>> module.weight.grad.data
AttributeError: 'NoneType' object has no attribute 'data'
>>> module.weight.grad + 1.0
TypeError: unsupported operand type(s) for +:
'NoneType' and 'float'
```

</td>
</tr>
</table>

### **Update `torch.tensor` and `nn.Parameter` to serialize all their attributes (#88913)**

Any attribute stored on `torch.tensor` and `torch.nn.Parameter` will now be serialized. This aligns the serialization behavior of `torch.nn.Parameter`, `torch.Tensor` and other tensor subclasses

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
# torch.Tensor behavior
>>> a = torch.Tensor()
>>> a.foo = 'hey'

>>> buffer = io.BytesIO()
>>> torch.save(a, buffer)
>>> buffer.seek(0)
>>> b = torch.load(buffer)

>>> print(a.foo)
hey
>>> print(b.foo)
AttributeError: 'Tensor' object has no attribute 'foo'

# torch.nn.Parameter behavior
>>> a = nn.Parameter()
>>> a.foo = 'hey'

>>> buffer = io.BytesIO()
>>> torch.save(a, buffer)
>>> buffer.seek(0)
>>> b = torch.load(buffer)
>>> print(a.foo)
hey
>>> print(b.foo)
AttributeError: 'Parameter' object has no attribute 'foo'

# torch.Tensor subclass behavior
>>> class MyTensor(torch.Tensor):
...   pass

>>> a = MyTensor()
>>> a.foo = 'hey'
>>> print(a.foo)
hey

>>> buffer = io.BytesIO()
>>> torch.save(a, buffer)
>>> buffer.seek(0)
>>> b = torch.load(buffer)
>>>print(b.foo)
hey
```

</td>
<td>

```Python
# torch.Tensor behavior
a = torch.Tensor()
a.foo = 'hey'

>>> buffer = io.BytesIO()
>>> torch.save(a, buffer)
>>> buffer.seek(0)
>>> b = torch.load(buffer)
>>> print(a.foo)
hey
>>> print(b.foo)
hey

# torch.nn.Parameter behavior
>>> a = nn.Parameter()
>>> a.foo = 'hey'

>>> buffer = io.BytesIO()
>>> torch.save(a, buffer)
>>> buffer.seek(0)
>>> b = torch.load(buffer)
>>> print(a.foo)
hey
>>> print(b.foo)
hey

# torch.Tensor subclass behavior
>>> class MyTensor(torch.Tensor):
...   pass

>>> a = MyTensor()
>>> a.foo = 'hey'
>>> print(a.foo)
hey

>>> buffer = io.BytesIO()
>>> torch.save(a, buffer)
>>> buffer.seek(0)
>>> b = torch.load(buffer)
>>>print(b.foo)
hey
```

</td>
</tr>
</table>

If you have an attribute that you don't want to be serialized you should not store it as an attribute on tensor or Parameter but instead it is recommended to use `torch.utils.weak.WeakTensorKeyDictionary`

```Python
>>> foo_dict = weak.WeakTensorKeyDictionary()
>>> foo_dict[a] = 'hey'
>>> print(foo_dict[a])
hey
```

### **Algorithms `{Adadelta, Adagrad, Adam, Adamax, AdamW, ASGD, NAdam, RAdam, RMSProp, RProp, SGD}` default to faster `foreach` implementation when on CUDA + differentiable=`False`**

When applicable, this changes the default behavior of `step()` and anything that calls into `adadelta(...)`, `adagrad(...)`, `adam(...)`, `adamax(...)`, `adamw(...)`, `asgd(...)`, `nadam(...)`, `radam(...)`, `rmsprop(...)`, `rprop(...)`, `sgd(...)` directly to use the `foreach` implementation instead of the for-loop for better performance. However, this change can potentially be backward incompatible since there may be small numerical differences between the results computed with the `foreach` implementation and the previous default. The foreach implementation will be the default only if the following conditions are met.

1. The user has not specified kwargs relating to implementation (`foreach`, `fused`, or `differentiable`),
2. All tensors are native tensors (not subclasses) and on CUDA,
3. `torch.jit.is_scripting` is `False`.

When these conditions are satisfied, the implementation used will match the implementation used when one passes `foreach=True`. The user defined flag for `foreach` will NOT be overwritten in order to preserve user selections. For more details, check the [documentation](https://pytorch.org/docs/stable/optim.html#algorithms). There should be no significant differences between the results returned by these optimizers. To revert to the old behavior, say, for `adam`, pass in `adam(..., foreach=False, ...)` or initialize `Adam` with `Adam(..., foreach=False, ...)`.

Pull Requests: #92306, #92716, #92723,#92724, #92726, #92727, #92728, #92715, #91896, #92730, #90865, #93184, #92181, #92923, #95415, #95818, #95811

### **`torch.nn.utils.stateless.functional_call` now respects tied weights (#90477)**

Assume a module has two tied weights, x and x_tied. Previously, invoking `functional_call(module, parameters_and_buffers, args, kwargs=None, *, strict=False)` with a parameter dictionary of only one of the tied weights would result in the other one(s) not being updated.

We’ve changed the behavior so that providing one of the tied weights in the parameter dictionary will update all other tied weights. If you would like the behavior in previous versions of PyTorch, please set `tie_weights=False`.

Please also see the related deprecation section "torch.nn.stateless.functional_call in favor of torch.func.functional_call".

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
>>> class Foo(nn.Module):
...    def __init__(self):
...        super().__init__()
...        self.x = nn.Parameter(torch.zeros([]))
...        self.x_tied = self.x
...
...    def forward(self, inp):
...        return self.x + self.x_tied

>>> foo = Foo()
>>> params = {'x': torch.ones([])}
>>> result = functional_call(foo, params, torch.randn([]))
>>> print(result)
1.0
```

</td>
<td>

```Python
>>> class Foo(nn.Module):
...    def __init__(self):
...        super().__init__()
...        self.x = nn.Parameter(torch.zeros([]))
...        self.x_tied = self.x
...
...    def forward(self, inp):
...        return self.x + self.x_tied

>>> foo = Foo()
>>> params = {'x': torch.ones([])}
>>> result = functional_call(foo,
...                         params,
...                         torch.randn([]),
...                         tie_weights=False)
>>> print(result)
1.0
```

</td>
</tr>
</table>

### **Require `return_complex` to be passed explicitly to `torch.stft` for real input (#86724)**

`torch.stft` takes an optional return_complex parameter that indicates whether the output should be a floating point tensor or a complex tensor. `return_complex` previously defaulted to False for real input tensors. This PR removes the default and makes `return_complex` a required argument for real inputs. However, complex inputs will continue to default to `return_complex=True`.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
>>> a = torch.rand(1024)
>>> _ = torch.stft(a, n_fft=128)
```

</td>
<td>

```Python
>>> t = torch.rand(1024)
>>> _ = torch.stft(t, n_fft=128, return_complex=False)
```

</td>
</tr>
</table>

### **Require inputs to `torch.istft` to be complex valued**

`torch.istft` no longer supports input in the form of real tensors
with shape `(..., 2)` to mimic complex tensors. Instead, convert
inputs to a complex tensor first before calling `torch.istft`.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
>>> t = torch.rand(65, 33, 2)
>>> _ = torch.istft(t, n_fft=128, length=1024)
```

</td>
<td>

```Python
>>> t = torch.rand(65, 33, 2)
>>> _ = torch.istft(t, n_fft=128, length=1024)
RuntimeError: istft requires a complex-valued input
tensor matching the output from stft with return_complex=True.
>>> t_complex = torch.view_as_complex(t)
>>> _ = torch.istft(t_complex, n_fft=128, length=1024)
```

</td>
</tr>
</table>

### **Change default behavior of sparse tensor construction to not do component verification(#92094)**

We now disable the costly component verification of torch.sparse_coo/csr/csc/bsr/bsc/compressed_tensor by default. The user can use the new `check_invariants` flag or `torch.sparse.check_sparse_tensor_invariants` to locally enable component verification. This allows users to constrain these costly checks to specific regions of their code and enables better overall performance. Previously users had no access to public constructors that disable these checks.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
>>> i = [[0, 1, 1],
         [2, 0, 5]]
>>> v =  [3, 4, 5]
>>> s = torch.sparse_coo_tensor(i, v, (2, 3))
RuntimeError: size is inconsistent with
indices: for dim 1, size is 3 but found index 5
```

</td>
<td>

```Python
>>> i = [[0, 1, 1],
         [2, 0, 5]]
>>> v =  [3, 4, 5]
>>> s = torch.sparse_coo_tensor(i,
...                            v,
...                            (2, 3),
...                            check_invariants=True)
RuntimeError: size is inconsistent with indices: for
dim 1, size is 3 but found index 5
>>> with torch.sparse.check_sparse_tensor_invariants():
...     s = torch.sparse_coo_tensor(i, v, (2, 3))
...
RuntimeError: size is inconsistent with indices: for
dim 1, size is 3 but found index 5
```

</td>
</tr>
</table>

### **Remove deprecated functionality from `torch.testing`**

Historically, `torch.testing` exposed a lot of private and undocumented functionality publicly. The 2.0 release completes the deprecation cycle for the following items and removes them:

- `rand` and `randn` (#87970)
- `get_all_device_types` (#87971)
- multiple dtype getters (#87972)
- `make_non_contiguous` (#87973)

### **Hooks registered on tensor to always run, even if they are the inputs to `.grad()` (#85849)**

This is a bug fix. Per the docs, hooks registered to Tensor should fire any time gradients are computed w.r.t. to that tensor. This change corrects the behavior to be consistent with the documentation. See [documentation](https://pytorch.org/docs/2.0/notes/autograd.html#backward-hooks-execution) for more details about backward hooks execution..

**2.0**

```Python
a = torch.tensor(1., requires_grad=True)
b = a.clone()
b.register_hook(hook)  # the hook registered here didn't fire before!
torch.autograd.grad(b.clone(), inputs=(b,))
```

### **`grad_fn` post-hooks can always observe the modifications to gradient by any grad_fn pre-hooks or hooks registered to Tensor, even if this is a leaf tensor (#85849)**

This corrects the behavior of hooks to be consistent with the documentation in the case where the tensor is a leaf tensor, i.e. the node is a grad accumulator node. See [documentation](https://pytorch.org/docs/**2.0**/notes/autograd.html#backward-hooks-execution) for more details about backward hooks execution.

**2.0**

```Python
def hook(grad):
   # updates grad
   return grad * 3

def hook2(grad_input, grad_output):
   # Before this change, grad_output would NOT see the x3
   print(grad_output)

a = torch.tensor(1., requires_grad=True)
b = a.clone()
acc_grad = b.grad_fn.next_functions[0][0]
acc_grad.register_hook(hook2)
b.register_hook(hook)
torch.autograd.backward(b.clone(), inputs=(a,))  # hook fire
```

### **Remove FSDP `params_with_grad` (#87480)**

In FSDP, we used to have an API `params_with_grad` for users to get parameters which have gradients from the FSDP module. We decided not to expose this helper because it is not a common paradigm.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
m = FullyShardedDataParallel(module)
m.params_with_grad()
```

</td>
<td>

```Python
m = FullyShardedDataParallel(module)
m.params_with_grad()  # Runtime error thrown
# For work-around, users can still do
[p for p in self.parameters() if p.grad is not None]
```

</td>
</tr>
</table>

### **Users doing wildcard import of torch.distributed.fsdp.fully_sharded_data_parallel will no longer get non-public symbols (#87917)**

Users could previously import both public and non-public symbols:

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
from torch.distributed.fsdp.fully_sharded_data_parallel import *
ShardingStrategy.FULL_SHARD # Non-public API
FullyShardedDataParallel(module) # public API
```

</td>
<td>

```Python
from torch.distributed.fsdp.fully_sharded_data_parallel import *
ShardingStrategy.FULL_SHARD # Non-public API, this will fail now
Fully`Sharded`DataParallel(module) # public API
...
# Users can instead
from torch.distributed.fsdp.fully_sharded_data_parallel import (
FullyShardedDataParallel,
ShardingStrategy,
)
FullyShardedDataParallel(module, sharding_strategy=ShardingStrategy.FULL_SHARD)
```

</td>
</tr>
</table>

### **Signature of FSDP `auto_wrap_policy `related APIs were changed in (#88450).**

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
lambda_auto_wrap_policy(m, unwrapped_params=...)
transformer_auto_wrap_policy(m, unwrapped_params=...)
size_based_auto_wrap_policy(m, unwrapped_params=...)
```

</td>
<td>

```Python
lambda_auto_wrap_policy(m, nonwrapped_numel=...)
transformer_auto_wrap_policy(m, nonwrapped_numel=...)
size_based_auto_wrap_policy(m, nonwrapped_numel=...)
```

</td>
</tr>
</table>

### **Updated `alltoall` signature to be consistent with other c10d APIs (#90569)**

The keyword argument names have been changed.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
alltoall(output=..., input=...)
```

</td>
<td>

```Python
alltoall(output_tensors=..., input_tensors=...)
```

</td>
</tr>
</table>

### **Remove unused functions in torch.ao.quantization.fx.utils (#90025)**

This commit removes the following unused functions from both the torch.quantization and the
torch.ao.quantization namespaces:

- `graph_pretty_str`
- `get_per_tensor_qparams`
- `quantize_node`
- `get_qconv_op`
- `create_qparam_nodes`
- `node_return_type_is_int`
- `is_get_tensor_info_node`

### **Make `torch.ao.quantization.backend_config.BackendConfig` accept inputs in the right order (#90698)**

The existing `BackendConfig` fusion pattern uses a "reversed nested tuple" format that is unintuitive.
This pattern format also complicates the signatures of the user specified "fuser methods", which needed to accept arguments in reverse nested order to match
the patterns:

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
import torch as nn
import torch.ao.nn.intrinsic as nni
from torch.ao.quantization.backend_config import (
  BackendPatternConfig
)
def fuse_linear_relu(is_qat, relu, bn_conv):
    (bn, conv) = bn_conv
    return nni.ConvBnReLU2d(conv, bn, relu)

config = (
    BackendPatternConfig((nn.ReLU, (nn.BatchNorm2d, nn.Conv2d)))
    .set_dtype_configs(...)
    .set_fuser_method(fuse_conv_bn_relu)
    .set_fused_module(nni.ConvBnReLU2d)
)

backend_config.configs  # returns Dict[Pattern, BackendPatternConfig]
```

</td>
<td>

```Python
def fuse_linear_relu(is_qat, conv, bn, relu):
    return nni.ConvBnReLU2d(conv, bn, relu)

config = (
    BackendPatternConfig((nn.Conv2d, nn.BatchNorm2d, nn.ReLU))
    .set_dtype_configs(...)
    .set_fuser_method(fuse_conv_bn_relu)
    .set_fused_module(nni.ConvBnReLU2d)
)

# Or for backward-compatibility
def fuse_linear_relu(is_qat, relu, bn_conv):
    (bn, conv) = bn_conv
    return nni.ConvBnReLU2d(conv, bn, relu)

config = (
    BackendPatternConfig()
    ._set_pattern_complex_format((nn.ReLU, (nn.BatchNorm2d, nn.Conv2d)))
    .set_dtype_configs(...)
    .set_fuser_method(fuse_conv_bn_relu)
    .set_fused_module(nni.ConvBnReLU2d)
)

backend_config.configs  # returns List[BackendPatternConfig]
```

</td>
</tr>
</table>

### **Make the AO codebase compliant with the public vs private API guidelines of pytorch [Public-API-definition-and-documentation](https://github.com/pytorch/pytorch/wiki/Public-API-definition-and-documentation)**

If users were using any of the AO private APIs then these would have to be accessed with a preceding `_` to conform with the guidelines.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
get_observer_dict()
```

</td>
<td>

```Python
_get_observer_dict()
```

</td>
</tr>
</table>

Pull Requests: (#86029, #87515, #87516, #87517, #87518, #87519, #88392, #88394, #88396, #88397, #87521, #88395, #87883, #88399, #88398, #86022, #86023, #86024, #86025, #86026, #86027, #86028, #86030, #86031, #86032, #86033, #86034, #86037, #90315, #88391, #90554, #87520)

### **Remove overwrite_output_observer and represent the observer constraints for fixed qparams ops through the existing DTypeWithConstraints mechanism (#88620)**

This commit removes `overwrite_output_observer` and `overwrite_output_fake_quantize` overwrite observer settings in the BackendConfig. Instead, we represent the observer constraints for
fixed qparams ops through the existing DTypeWithConstraints mechanism. Note that, however, to be consistent with other DTypeWithConstraints checks, we no longer throw an error if an incorrect observer is specified, but simply ignore the offending QConfig and log a warning instead. This is the BC-breaking part of the change.
**1.13**

```Python
from torch.ao.quantization.qconfig import default_qconfig
from torch.ao.quantization.quantize_fx import prepare_fx

model = ModelWithFixedQParamsOps()
qconfig_mapping = QConfigMapping().set_global(default_qconfig)
example_inputs = ...
prepare_fx(model, qconfig_mapping, example_inputs)
```

Before this commit, running the above leads to an exception because the wrong observers are used for fixed qparams ops. After this commit, the above will only encounter a warning,and the fixed qparams ops will not be quantized. In both cases, switching to `get_default_qconfig_mapping` will cause the fixed qparams ops to be quantized.

### **Remove `torch.ao.quantization.quantization_patterns` and `torch.ao.quantization.fusion_patterns`(#89872)**

The following classes under the `torch.ao.quantization.fx.quantization_patterns` namespace are migrated to the `torch.ao.quantization.fx.quantize_handler`
namespace:

- `QuantizeHandler`
- `BinaryOpQuantizeHandler`
- `CatQuantizeHandler`
- `ConvReluQuantizeHandler`
- `LinearReLUQuantizeHandler`
- `BatchNormQuantizeHandler`
- `EmbeddingQuantizeHandler`
- `RNNDynamicQuantizeHandler`
- `DefaultNodeQuantizeHandler`
- `FixedQParamsOpQuantizeHandler`
- `CopyNodeQuantizeHandler`
- `GeneralTensorShapeOpQuantizeHandler`
- `CustomModuleQuantizeHandler`
- `StandaloneModuleQuantizeHandler`

The following classes under the torch.ao.quantization.fx.fusion_patterns namespace are migrated to the torch.ao.quantization.fx.fuse_handler
namespace:

- `DefaultFuseHandler`
- `FuseHandler`

### **Remove public APIs under the `torch.ao.quantization.fx.backend_config_utils` namespace(#89810)**

The following APIs that were mistakenly public under the `torch.ao.quantization.fx.backend_config_utils` namespace are removed in this commit.

- `get_quantize_handler_cls`
- `get_fusion_pattern_to_fuse_handler_cls`
- `get_native_quant_patterns`
- `get_pattern_to_quantize_handlers`

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
from torch.ao.quantization.fx.backend_config_utils import (
    get_quantize_handler_cls,
    get_fusion_pattern_to_fuse_handler_cls,
    get_native_quant_patterns,
    get_pattern_to_quantize_handlers,
)
all_quant_patterns = get_native_quant_patterns()
```

</td>
<td>

```Python
from torch.ao.quantization.fx.quantization_patterns import (
    _get_quantize_handler_cls,
    _get_pattern_to_quantize_handlers,
)
from torch.ao.quantization.fx.fusion_patterns import (
    _get_fusion_pattern_to_fuse_handler_cls,
)
from torch.ao.quantization.backend_config import (
    get_native_backend_config,
)
all_quant_patterns = _get_pattern_to_quantize_handlers(
    get_native_backend_config()
)
```

</td>
</tr>
</table>

### **Update torch.{slice|select|diagonal|as_strided}\_scatter ops to preserve input stride/storage_offset (#91029)**

These operators are primarily used by the [functionalization pass](https://dev-discuss.pytorch.org/t/functionalization-in-pytorch-everything-you-wanted-to-know/965), used in AOTAutograd. Previously, they would always return contiguous tensors. Now, they return a tensor with the same striding as their first argument.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
>>> x = torch.ones(2, 2, 2)
>>> base = x[:, :, 1]
>>> base.stride()
(4, 2)
>>> x = torch.zeros(2, 2, 2)
>>> base = x[:, :, 1]
>>> base.stride()
(4, 2)
>>> torch.diagonal_scatter(base, torch.ones(2)).stride()
# returns a tensor with same strides as base.
(4, 2)
```

</td>
<td>

```Python
>>> x = torch.ones(2, 2, 2)
>>> base = x[:, :, 1]
>>> base.stride()
(4, 2)
>>> x = torch.zeros(2, 2, 2)
>>> base = x[:, :, 1]
>>> base.stride()
(4, 2)
>>> torch.diagonal_scatter(base, torch.ones(2)).stride()
# returns a contiguous tensor
(2, 1)
```

</td>
</tr>
</table>

### **Remove ONNX deprecated monkey patches to torch.Graph (#94747)**

The Deprecated monkey patches to `torch.Graph`, `torch.Block` and `torch.Node` are removed

Monkey patches to the classes `torch.Graph`, `torch.Block` and `torch.Node` from `torch.onnx` have been removed. This means the methods `torch.Graph.op()`, `torch..Graph.at()`, `torch.Block.op()`, `torch.Graph.constant()`, and `torch.Node.__getitem__` are no longer available.

Users creating custom symbolic functions for the `torch.onnx` exporter can continue to assume the `g.op()` interface for creating an operator in the graph, which is now exposed via the `GraphContext` class. Users should not assume any other methods from the `GraphContext` class other than those defined natively by `torch.Graph` and `.op()`.

Code change to existing symbolic functions is not expected with this change.

### **Add full checker mode in torch.onnx.export (#83186)**

This removes boolean value of `full_check` parameter in TORCH API `check_onnx_proto`, and forces `full_check` with warning messages if it fails.

Also, the API didn’t check on types in the graph even with `full_check=True` previously. With the change, a warning message will show if the graph contains type error.

### **C++ API specific BC-Breaking Changes:**

#### **Deleted torch::deploy from PyTorch Core (#85953)**

`torch::deploy` has been migrated to over to [MultiPy](https://github.com/pytorch/multipy). Ongoing development will continue in this repository.

#### **Remove the use of `lazy::View` (#87822)**

The view and aliasing infrastructure in lazy tensor core has been deprecated in favor of functionalization.

#### **Renamed `c10::fromIntArrayRef` to `c10::fromIntArrayRefSlow` and changed call sites (#86235)**

The function has been renamed to more accurately reflect its performance characteristics.

# Deprecations

## torch.func aka functorch

### **We’ve deprecated the functorch module in favor of the new torch.func module**

We’re excited to announce that, as the final step of upstreaming and integrating functorch into PyTorch, the functorch APIs are now available in the torch.func module. Our function transform APIs are identical to before, but we have changed how the interaction with NN modules work.

We’ve deprecated `functorch._` function transforms (e.g. `vmap`, `grad`, `jvp`) in favor of their identical `torch.func._ `counterparts (#92279).
PyTorch has consolidated on `torch.func.functional_call` as the NN module functional API. Please migrate from `functorch.{make_functional, make_functional_with_buffers}` to it. For more details see this [Guide](https://pytorch.org/docs/master/func.migrating.html#functorch-make-functional)
Please migrate from `functorch.combine_state_for_ensemble` to `torch.func.stack_module_state`. For more details see this [Guide](https://pytorch.org/docs/master/func.migrating.html#functorch-combine-state-for-ensemble)
We are no longer supporting functorch.compile (also known as AOTAutograd) as a frontend for compilation in PyTorch; we have integrated AOTAutograd into PyTorch’s compilation story. If you are a user, please use `torch.compile()` instead.

## Python API

### **Deprecate TypedStorage, its derived classes, and all of their public methods (#85303)**

Typed storages have been removed from the C++ side and torch.UntypedStorage is used in place. The use of torch.TypedStorage and all of its subclasses is now deprecated.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
tensor.storage()
torch.TypedStorage(...)
```

</td>
<td>

```Python
tensor.untyped_storage()
torch.UntypedStorage(...)
```

</td>
</tr>
</table>

If you need to access individual elements in a storage as a particular dtype, you can simply create a tensor to view it:

```Python
torch.tensor(storage, dtype=...)
```

### **Deprecate `tensor.mT`,`tensor.T`,`tensor.mH`,`tensor.H` on 0D-tensors (#92143)**

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
>>> a = torch.tensor(10)
>>> a.T
>>> a.H
```

</td>
<td>

```Python
>>> a = torch.tensor(10)
>>> a.T
UserWarning: Tensor.T is deprecated on 0-D tensors.
This function is the identity in these cases.
>>> a.H
UserWarning: Tensor.H is deprecated on 0-D tensors.
Consider using x.conj().
```

</td>
</tr>
</table>

## Autograd API

### **Deprecate decorating classes with torch.no_grad (#89522)**

Decorating classes with `torch.no_grad` is now deprecated. You should be decorating its functions or methods instead. To preserve the current behavior of class decoration, you can directly decorate the `__init__` method and nothing else.

<table>
<tr>
<th>1.13</th>
<th>2.0</th>
</tr>
<tr>
<td>

```Python
@torch.no_grad()
class Blah():
  pass
```

</td>
<td>

```Python
class Blah():
  @torch.no_grad()
  def __init__(self):
    pass
```

</td>
</tr>
</table>

## Linalg

### **Remove the use of overload at::frobenius_norm(const Tensor&) (#81762)**

In continuation with the deprecation process from release 1.12 the tensor overload for this function has been removed. This function was not used in the bindings of Pytorch and should not impact users of `torch.norm`.

## torch.nn API

### **Canceling deprecation of `functional.{tanh, sigmoid}` functions (#86905)**

Both these ops are heavily used and so will not be removed. Deprecation warnings have been removed.

### **Deprecated torch.nn.utils.stateless.functional_call in favor of torch.func.functional_call (#92280)**

We’ve moved torch.nn.stateless.functional_call under the torch.func module to reflect how it is useful for working with nn.Modules in a functional style. As of PyTorch **2.0**, `torch.func.functional_call` is a drop-in replacement for `torch.nn.stateless.functional_call` and we will remove `torch.nn.utils.stateless.functional_call` in a future version of PyTorch. However, please note that we did change the default behavior of `torch.nn.stateless.functional_call` in PyTorch 2.0 (see “torch.nn.utils.stateless.functional_call now respects tied weights” under BC-breaking notes).

## Releng

### **Deprecated private API torch.\_six (#94709)**

Removed the Python 2 and 3 compatibility library six and future and torch.\_six.
**2.0**

```Python
# from torch._six import string_classes
str
# from torch._six import int_classes
int
# from torch._six import inf, nan
from torch import inf, nan
# torch._six.string_classes
str
```

## Onnx

### **Deprecated Caffe2 ONNX exporter support[ #95071](https://github.com/pytorch/pytorch/pull/95071)**

Users must use PyTorch 1.x versions to use Caffe2 ONNX exporter. This capability will be completely removed from PyTorch 2.x series.

# New Features

## torch.nn API

- Add `torch.nn.functional.scaled_dot_product_attention()` to allow writing fast Transformer-like functions and use it to speed up `nn.Transformer()` ( #91362, #91066, #90413, #87312, #94008, #89470, #90776, #92189)
- Add hooks for `Module.register_{buffer,module,parameter}` functions (#86148, #87369)
- Add `Module.full_backward_pre_hook` (#86700)
- Add `Module.state_dict_pre_hook` (#90435)
- Add `Module.call_super_init: bool` flag that can be used to ensure `Module` initialization is properly calling parent’s `__init__` (#91819)

## torch.func

- Add `functorch` support [for torch.autograd.Function](https://pytorch.org/docs/master/notes/extending.func.html): one is now able to apply function transformations (e.g. vmap, grad, jvp) over torch.autograd.Function. (#92023, #91452, #91222, #90037, #90077, #90966, #89860, #91211, #92030)
- Add support for linearize a-la [jax.linearize](https://jax.readthedocs.io/en/latest/_autosummary/jax.linearize.html#jax.linearize) (#94173)
- Add torch.func.functional_call, a new utility function to work with NN modules. (#89213)
- Add torch.func.stack_module_state, a new utility function to help with model ensembling (#88850)

## Cuda

- Introduce CUDA Device Assertions Infrastructure (#84609)
- `Logcumsumexp` for complex dtypes for CUDA (build-time optimized) (#94310)
- Caching allocator tracing (#86241)
- Add Pluggable CUDA allocator backend (#86786)
- Add cudaMallocAsync as an alternative backend for the CUDA allocator (#82682)

## Cpp API

- Add `set_to_none` flag for C++ optim endpoint (#92989)

## NestedTensor API

- Add support for `tensor.to()` for NestedTensor backend (#87146)
- Add backwards support for `gelu` and `relu` operators (#94776)
- Add support for `torch.neg` operator (#88131)

## Distributed

- Distributed Tensor (Prototype Release)
  - PyTorch [DistributedTensor](https://github.com/pytorch/pytorch/blob/master/torch/distributed/_tensor/README.md) (DTensor) is a prototyping effort with distributed tensor primitives to allow easier distributed computation authoring in the SPMD (Single Program Multiple Devices) paradigm. The primitives are simple but powerful when used to express tensor distributions with both sharded and replicated parallelism strategies. PyTorch DTensor empowered PyTorch [Tensor Parallelism](https://pytorch.org/docs/master/distributed.tensor.parallel.html) along with other advanced parallelism explorations. In addition, it also offers a uniform way to save/load state_dict for distributed checkpointing purposes, even when there’re complex tensor distribution strategies such as combining tensor parallelism with parameter sharding in FSDP. (#88176, #88177, #88178, #88179, #88551, #88549, #88550, #89800, #89967, #89968, #89991, #90106, #90241, #90449, #90731, #90732, #90733, #90734, #90735, #91756, #91783, #91785, #91801, #91802, #92069, #92197, #92198, #92290, #92611, #92651, #92652, #92677, #93040, #93160, #93306, #93832, #93957, #94517, #94524)
  - We also design and implement Tensor Parallel & 2D Parallel (Tensor Parallel + FSDP) on top of DistributedTensor. (#88180, #89242, #89467, #89535, #89779, #89878, #93029, #93412, #94421, #94748)
- Distributed Checkpoint
  - PyTorch Distributed Checkpointing (DCP) API was first introduced in PyTorch 1.13 and this will be an official prototype release in PyTorch 2.0. The distributed checkpoint API in PT2.0 decouples the storage layer from the checkpoint planning layer. Planner types are introduced to perform the coordination of storage both locally and globally to plan the save/load process. Checkpointing support for FSDP `sharded_state_dict` is added as well. (#87987, #88698, #89256, #89398, #89399, #89501, #89503, #89537, #89542, #89873, #89964, #90212, #91036, #91092, #91209, #91269, #92553, #92705, #92829, #92869, #92933, #94379, #94501)
- DistributedDataParallel
  - Enable DDP for PyTorch 2.0 (#87549, #88523, #89096, #88460, #88480, #88521, #94749, #93162, #89802, #92986)
- FullyShardedDataParallel
  - Add the option to use the original parameters via `use_orig_params=True` in the FSDP constructor (#84911)
  - Enable the use of TorchDispatch with FSDP (#88014)
  - Hybrid Sharded Data Parallel (#89915)
  - Enable FSDP for PyTorch 2.0 (#88781, #89330, #89523)
- Distributed (c10d)
  - Dispatchable collectives: An improvement to the existing `init_process_group` API which changes backend to an optional argument. For users, this feature will allow for code that runs on both GPU and CPU machines without having to change the backend specification. The dispatchability feature will also allow users to perform both GPU and CPU collectives using the same ProcessGroup, as PyTorch will automatically find an appropriate backend for the tensor type (as of PyTorch 2.0, the default is NCCL for CUDA and Gloo for CPU). Existing backend specifications by users will be honored and will not require change (#83679, #83735, #83810, #83859, #83876, #83916, #84423, #86166, #86368, #86407, #86408, #86409, #88351, #88846, #88889, #88903, #89317, #89318, #89505, #89813, #88330, #91257, #91172)

## Mps

- Add native support for:`torch.nn.functional.group_norm`(#91190), `torch.var_mean` (#91190), `torch.nansym`(#93845), `torch.frac`(#86625), `torch.signbit`(#87214), `torch.exp1m`(#87147), `torch.cumsum`(#88319), `torch.trace`(#87910), `torch.nn.Hardswish` (#87952),`torch.inverse`(#90428), `torch.floor_divide`(#91126), `unfold`(#91266), `bincount`(#91267), `nonzero`(#91616), `norm_dtype`and`cdist`(#91643), `unique`and`unique_consecutive`(#88532), `nan_to_num`(#91110), `torch.linalg.cross`(#91642), `randperm`(#91708), `triangular_solve`(#94345), `grid_sampler2d`(#94273), `remainder`(#92139), `addr`(#94538), `fmod`(#94722), `repeat_interleave` (#88649),`sort`and`argSort`(#94697),`range` (#91075)
- Add functions to handle rng and force device synchronization `torch.mps.{get_rng_state, set_rng_state, synchronize, manual_seed, seed}` (#94417)
- Add support for the `mps` device for `torch.Generator` (#91348)
- Add `torch.int64` support for unary ops (#86615)

## Profiler

- Improve Memory Profiler(alpha): enhancement to the existing memory profiler that can attribute memory consumptions to activations, gradients, parameters, and optimizer states (#86802, #86853, #86854, #86880, #87006, #87566, #87567, #87568, #88924, #88925, #88926, #89355, #89356, #86355, #88917, #87133, #86753, #86754, #87096, #86909, #87825)
- Add Linux perf event support in profiler (#87866, #87874)

## Foreach API

- Implement:
  - `torch._foreach_lerp` (#87562),
  - `fused adamw` (#88015)
  - `_foreach_addc`(div/mul)(\_).Tensor (#88157)
  - `clamp_min` `clamp_max` (#91384)
  - `adamw` (#88015)

## Mobile

- Add XNNPACK Delegate Framework.
  - Enable a XNNPACK graph to be built from the torchscript IR and performing checks (#86980, #87128, #87824)
  - Add flatbuffer serialization support (#87826, #87906, #87907, #87908)
  - Create `Executor` and `Compiler` classes which compiles the XNNPACK graph and preps for execution (#88779, #88778, #88780, #89090)
  - Optimize library includes (#88863, #89231)
  - Add Constant Data which will be used in Convolution (#89445)
- Add support for better benchmarking
  - Add support in lite_predictor benchmark binary to select event lists and perform benchmarking using Linux perf through Kineto profiler (#87876)
  - List all missing ops at once (#94205)

## Sparse API

- Add `torch.sparse.check_sparse_tensor_invariants` context manager that allows users to opt into more checks at runtime for better debugging. (#92094)
- Add `check_invariants` flag to `torch.sparse_coo/csr/csc/bsr/bsc/compressed_tensor `to allow users to verify components at construction time. (#92094)
- Add `reduce` flag for CPU to torch.sparse.mm with support for `sum, mean, amax, amin` (#83727)

## Optimizer API

- Make `{Adadelta, Adagrad, Adamax, AdamW, ASGD, NAdam, RAdam, RProp}` differentiable (#86096, #86258, #86183)
- Publicly expose \_LRScheduler to LRScheduler (#88503)

## Distributions

- Add a transform for positive-definite matrices. (#76777)

## Signals

- Set up new module torch.signal.windows (#85599)
- Add the Nuttall window to signals/ (#90103)
- Implement old singal/windows in Python (#87082, #87330)

## Quantization

- Add support for oneDNN backend for server CPU quantized inference (#91056, #88478, #88665, #88668, #88879, #88923, #89188, #91297, #90262, #90364, #91152, #91153, #91154, #91155, #91934, #88661)
- Add new ‘x86’ backend to be used for quantized CPU inference (#91235, #88799)

## Vulkan

- Add Vulkan support for several torch operators:
  - `torch.abs` (#87414)
  - `torch.select` for height and width dimensions (#94612)
- Vulkan optimization passes now automatically apply data transfers between the CPU and GPU for input and output tensors (#87432)
  - If the `requires_backend_transfers` flag of a model is set to `false`, then input tensors do not to be transferred to the GPU (via `tensor.gpu()`) and output tensors do not to be transferred back to the CPU (via `tensor.cpu()`) since these transfers are inserted into the model
  - To avoid inserting data transfers into a model, add `MobileOptimizer.VULKAN_AUTOMATIC_GPU_TRANSFER` under `torch.utils.mobile_optimizer` to the `optimization_blocklist` argument of `optimize_for_mobile` (#92081)

## ROCm

- `hipGraph` support for pytorch mainline (#88202)

## Fx

- Introduce symbolic shape guards (#87570, #90528, #90665, #90679, #90876, #91058, #93894, #94782)
- Introduce a match filter for SubgraphRewriter (#86430, #87998, #87257)
- Support list-typed args in PatternMatcher (#88656)
- Add `any_chain()` in operator support (#90949)
- Have replace_pattern return replaced nodes (#90244)

## Jit

- Allow freezing JIT modules that contain mutable interfaces (#86039, #91020)
- ApplyLinear-BatchNormNd folding during torch.jit.freeze (#86706)
- Add an option to skip loading of debug traces, in order to reduce memory usage (#91430)
- Introduce torch.jit.\_drop function modifier to avoid compiling a method on a non-nn.Module class (#93012)
- Allow providing a kwargs-like dict of example inputs to torch.jit.trace with the new `example_kwarg_inputs` argument (#81623, #94032)
- Include example input shapes when serializing jit.traced modules to assist with debugging (#90744)

## Build

- Add Ada Lovelace (cuda arch sm8.9) support (#87436)
- Add an option to disable TORCH_WARN and TORCH_WARN_ONCE log (#87188)
- Enable memory map file support for Android, Apple, and CXX (#88545)
- Support DNNL_GRAPH_CPU_RUNTIME=TBB build option (#87512)

## ONNX

- Verification tool to find mismatch in model export (#89946,[ #89807](https://github.com/pytorch/pytorch/pull/89807),[ #89808](https://github.com/pytorch/pytorch/pull/89808),[ #89947](https://github.com/pytorch/pytorch/pull/89947),[ #94648](https://github.com/pytorch/pytorch/pull/94648))

## Cudnn

- Add an environment variable to skip cudnn version compatibility check (#89184)
- Enable cuDNN Frontend v8 API by Default (#91117)

# Improvements

## Python API

- Set std/var correction overloads default value to None (#56398)
- Implement correction argument in torch.masked.{std,var} (#87118)
- Update `torch.squeeze` to allow squeezing multiple dimensions at once (#89017)
- Add support for int32 indices in index/index_put ops (#86309)
- Enable `where` to have cpu scalar args (#87022)
- Add support for NumPy scalars to `torch.tensor.asarray` (#90914)
- Update opt_einsum to have more reasonable defaults (#86985)
- Improve error message for `Tensor.set_` when dtypes mismatch(#88804)
- Enable out variant of `torch.max`(#85926)
- Implement faster gradient clipping using foreach function (#91846)

## Autograd API

- Add backward support for `torch.ormqr` (#86800)
- Pre-hooks registered on tensor are guaranteed to run before pre-hooks registered on grad_fn (#85849)
- Add a new overridable method `setup_context` (#89859, #92312)
  - You must use override this method if you plan to use your autograd Function with functorch
  - If you choose to override this method, `forward` should no longer take ctx as an input.
- Add context manager `torch.autograd.set_multithreading_enabled` for disabling multithreading in the autograd engine (#86245)
- Add backward AD support for unary foreach functions (#89591)

## torch.nn API

- Add `remove_duplicate` flag to `Module.named_buffers()` method (#84984) and `Module.named_parameters()` (#88090)
- Add kwarg support for `Module` forward-pre and forward hooks (#89389)
- Improve error message for `Transformer()` fast path (#90783) and kernel selection (#90783)
- Add support for `torch.bf16` for `Embedding` (#94163)
- Add `freeze` argument to `Embedding()` (#86769)
- Add `torch.channels_last_3d` support for `SyncBatchNorm()` (#88401)
- Add `torch.bfloat16` support on CPU for `functional.{mish,hardtanh,silu}` (#82460)
- Add support for inputs with different data types for `LayerNorm()` (#81851, #88064), `BatchNorm{1,2,3}d()` (#84410), `GroupNorm()` (#89485, #81852, #88663, #92671, #92668)
- Improve printing of `ModuleList()` (#90452)
- Add `torch.uint8` support for `functional.interpolate()` on CPU (#90771)
- Make `functional.max_pool1d` error checking consistent between CPU and CUDA (#90211)
- Add `SyncBatchNorm()` fallback to `BatchNorm()` when it is used in a non-distributed setting (#89706)
- Add channels-last support for `GroupNorm()` on XPU (#87680)
- Add `is_causal` kwarg to `TransformerEncoder()` layer (#90508)
- Add `prepend` argument to `Module` hooks to register a hook that will be called before the existing ones (#87370)

## Distributed

- Activation checkpointing
  - Return `None` from `apply_activation_checkpointing` (#87871)
  - Enable non-reentrant support for `checkpoint_sequential` (#86331)
  - Separate CPU offload activation to its own wrapper (#85459)
- DistributedDataParallel
  - Add `PackedSequence` support when `device_ids` is specified (#86614)
  - Enable DDP to handle custom dataclass forward outputs (#92334)
- Distributed (c10d)
  - Add sequence number support for UCC PG (#85047)
- FullyShardedDataParallel
  - Default to `BACKWARD_PRE` for the backward_prefetch of FSDP (#88428)
  - Skip collective communications for `NO_SHARD` in `clip_grad_norm_` (#89137)
  - Allow handle training state to be both `BACKWARD_PRE` and `BACKWARD_POST` in the post-backward assert (#89791)
  - Limit all gather after pre-unshard (#89057)
  - Include module classes in `ModuleWrapPolicy.__repr__` (#89058)
  - Apply the "largest" dtype across all parameters/gradients as defined by PyTorch's type promotion semantics for the total norm returned in `clip_grad_norm_` for low prec grads (#90028)
  - Introduce `ModuleWrapPolicy` for simplicity in FSDP autowrap (#88450)
  - Enable mixed hybrid/non-hybrid sharding strategies (#90846)
  - Re-support model dtype change after FSDP init (#91192)
  - Enable `use_orig_params=True`, `no_sync` and mixed precision to work together (#91193)
  - Enable `summon_full_params(with_grads=True)` (#85738, #87314)
  - Add `keep_low_precision_grads` support when CPU offloading (#86495)
  - Consolidate FSDP `state_dict` `offload_to_cpu` settings (#86211)
  - Add `set_state_dict_type` API to setup `state_dict_type` without using context manager (#86243)
  - Enable the support of `use_orig_param` for FSDP’s `optim_state_dict` (#89898, #89899, #89900)
  - Enable nested FSDP wrapper to use different mixed precision (#90523)
  - Enable input cast skip in MixedPrecision (#90620)
  - Publish `optim_state_dict` and `optim_state_dict_to_load` for FSDP (#90798, #91343, #92744, #92118, #92991, #92992, #93285, #93318, #94109, #94129)
  - Make default input casting in root module only and enable the ability to set different mixed precisions for different submodules (#91365)
- Torch Elastic
  - Update `torchrun` and `TorchElastic` to take optional `local_addr` param to allow skip local IP lookup if specified (#88922)

## torch.func

- Update vmap to accept None(s) in out_dim (#91644)
- torch.func.jacrev: Support chunked computation (#89376, #91326)
- vmap: chunk_size support (#91157)
- torch.vmap: Implement checks (rather than internal asserts) for vmap escaped errors (#89585)
- Avoid calling allclose in the backward if there are tensor subclasses (#91444)
- Refactor NN stateless APIs by swapping module tensors (#92536)

## Cuda

- Use binary units for CUDA memory summary (#91854)
- Improve perf by avoiding implicit string creation in c10_cuda_check_implementation (#88350)
- Add option to record C++ backtraces in \_record_memory_history (#86145)
- Set CUDA_MODULE_LOADING to LAZY when not set by the user (#85692)
- Add warning if captured graph is empty (#88754)
- Add option to dump a captured graph for debugging (#85519)
- Add support to foreach torch zero for bfloat16s (#90437)
- Enable bfloat16 for hardtanh_backward_cuda (#91511)
- Use pytree to allow any input format for cuda graph (#90941)
- Add requested_bytes to CUDA Caching Allocator Stats (#88575)
- Add an option to disable reduced precision reductions for BF16 GEMM (#89172)
- Add an env variable to disable addmm_cuda_lt kernel (#91436)

## Serialization

- Add XPU backend to support torch.save and torch.load (#89679)

## Cpp API

- Reduce ambiguity in Tensor namespace collisions (#92266)

## Dataloader API

- Add support for pin memory on xpu device (#86545)
- Add type annotation to `get_worker_info` (#87017)
- Allow prefetch factor to be optional (#88972)

## NestedTensor API

- Add add/mul for nested dense [B, *, D], [B, 1, D] case (CUDA-only) (#88289)
- Add support for torch.select over irregular dimensions (#88585)
- Add torch.nested.nested_tensor() constructor (#88213)

## Complex API

- Improve complex support for: `torch.nn.functional.conv_transpose3d `(#87967), `torch.log1p` (#89214,#90422), `torch.lerp` (#75584), `torch.logcumsumexp` for CPU (#93153)
- Solve under/overflow for complex division (#92539)

## Composability

- Improve coverage of primtorch and torch.\_ref decompositions: `prims.clone` (#86705), `ndtr, ndtri, log_ndtr, erfcx` (#86077), `NLL loss` (#81128), `conv backward` (#87047), `xlogy and xlog1py` (#77712), `alpha_dropout` (#87989)
- More operations now work with meta tensors: `_adaptive_avg_pool2d_backward` (#86359), (#87074), `avg_pool2d and avg_pool2d_backward` (#87043), `scalar_tensor and argmax` (#88590), `topk` (#88694), `max_pool2d_with_indices_backward` (#88743), `grid_sampler_2d_backward` (#88745), `linalg_cholesky` and `linalg_cholesky_ex` (#89430), `aten._cdist_forward` (#90042), `aten.pixel_shuffle` (#91605)

## Linalg API

- Fix typos in messages under aten (#88964)

## Mobile

- Improve CoreML logging and dependent libraries.
  - Updated Cocoapods (#88075)
  - Preserved CoreML errors by using special throw macro when encountering CoreML API errors (#86938)
- Clean Up MobileOptimizerType Rewrite Flags Public API and Documentation (#91600)
- Clean up flatbuffer lib dependency and fixed its test to match pkl models (#86041, #93022)
- Type corrections to avoid unnecessary static_casts (#93898)
- Add flake8-logging-format linter (#90805, #94840)

## Sparse API

- Add autograd support for `linear` (#86137, #86302), `mm`, `log1p`(#86301, #88155), `to_sparse_*`(#90281)
- Improve support for `sparse_dim`, `dense_dim` (#86203, #86203), `torch.sum`(#86300, #92979), torch.sparse.sampled_addmm`(#86401),`frac`, `deg2rad`, `rad2deg`, `relu`(#88153, #88156, #88442, #86749),`conj()`(#91695),`to_sparse`(#90718),`sparse_mask` (#92248, #94829)
- Add support for per batch index contiguity in CSR/CSC/BSR/BSC (#91243), non-contiguous values in CSR/CSC/BSR/BSC (#91243), non-zero dense_dim to COO/CSC/BSR/BSC/Strided conversions. (#90177), uncoalesced operands to `sparse_mask` (#91964)
- Improve error messages for `indices, values, (c)row_indices, (c)col_indices` (#93149) and `addmm` (#94843)
- Extend gradcheck to BSR and BSC inputs. (#90719)
- Sort BSR indices as part of CSR to BSR conversion (#90918)

## Cpu

- Implement aten::native_batch_norm.out for CPU (#88604)
- Log1p for complex in CPU (#89691)
- Enable oneDNN implementation for LSTM (#91158)

## Package

- Add better debugging for torch.package (#92939)

## Quantization

- Remove weight arg from DTypeConfig for non-weighted ops (#86335)
- Add get_symmetric_qnnpack_qconfig_mapping for XNNPACK quantized ops (#87002)
- Add assert for backend correctness in get_default_qconfig related apis (#86259)
- Replacing List[QConfigMapping] in parallel numeric profiler (#86922)
- Check the fixedqparam op qconfig based on backend_config (#87425)
- Explicitly set default quantized engine instead of relying on the order of supported_qengines (#89804)
- Support setting qconfig by module_type in QConfigMapping in PT 2.0 export flow (#92355)
- Migration of quantization code from torch._ to torch.ao._ (#86171, #86172)
- Improvements to qnnpack fully connected sparse ops (#85243, #85244, #85245, #85246, #85247)
- Support lowering of channel shuffle in FX (#83731)
- Remove explicitly default QConfigMapping settings (#90066)
- quant: make various configs printable (#91419)
- Enable FX quant for patterns like x.view(x.size(...), ...) (#90001)
- X86 qengine always uses fbgemm kernels on OS other than Linux (#93218)
- Change prepare_fx and convert_fx to preserve the GraphModule type of input (#94412)
- update xnnpack to newer version and update API usage in pytorch (#94330)
- Remove \_input_output_observed from backend_config (#92589)
- Add support for LSTM Structured Pruning prune_functions + pattern (#90801)
- Enable FX static quantization for LSTM (#85068)
- Allow setting fixed quantization params for inner LSTM ops (#88456)
- Add support for GRU in fx graph mode quantization (#91976)

## ONNX

- Operator support `col2im` opset 18 (#84594), `mse_loss` (#90717), `aten::contains` (#91660), src/index dynamic axes support for `aten::scatter_add` (#90090), `aten::zero` (#91731), Raise Unsupported for `GridSample` with volumetric 5D input (#92212)
- Pretty print diagnostic logging (#88261)
- Bump onnx to 1.13.1, onnxruntime to 1.14.0 (#90332,[ #94767](https://github.com/pytorch/pytorch/pull/94767))
- Add full graph checker option for `torch.onnx.export` API (#83186)
- Integrate all ONNX operators with a new `JitScalarType` API (#87245)
- Add `share_from_this` to `torch::jit::Graph` (#87343)
- Use optional op to keep None in results for ONNX internal tests (#84789)
- Add support for autograd function inlining in `ONNX_ATEN_FALLBACK` mode (#85736)
- Default runtime type checking to raising errors (#86555)
- Remove the `INT64_MAX` magic numbers (#88341)

## Fx

- Refactor graph partition to check for cyclic dependency (#86511)
- Enable nvprims.transpose fusions for nvFuser (#86967)
- Simplify magic method definition code. (#88017)
- Add sym_floor, sym_sqrt, sym_int (#88760)
- Propagate .meta info when replacing subgraphs in fx (#87255)
- Make `torch.fx` compatible with Python-3.11 (#92895)
- Add type(module) to be stored in the module stack (#87149)
- Ensure that symbolic variables incorporate fresh constraints before they're used (#87254)
- Add type annotation to `getitem` node before `split_module` (#88510)
- Implement pass for annotating getitem nodes (#90237)
- Guard Symbol and ShapeGuardPrinter behind HAS_SYMPY (#90704)
- Copy meta field in fx.GraphModule on deepcopy (#92062, #92623)
- Match get_attr when comparing nodes (#91657)
- Make **deepcopy** of fx.GraphModule handle circular reference. (#93038)
- Populate memo in deepcopy BEFORE copying children. (#93295)

## Mps

- Add fp16 support for `torch.nn.Linear` (#89774), `torch.nn.GELU` (#86218)
- Add support for empty Tensors in `torch.bitwise_not` (#87286), `torch.nn.LayerNorm` (#94212), many backward functions (#94343), `torch.nn.functional.hardswish` (#94342), `torch.topk` (#91884), `torch.arange` (#94485), `torch.linal.inv` (#94551),
- Improve error message for `nn.Conv2d` when inputs are on different devices (#86303)
- Add support via fallback for `torch.nn.{Fold, UnFold}` (#94491)
- Add support for reduction ops on multiple axis at a time (#91734)
- Add support for `k` greater than 16 for `torch.topk` (#94639)

## Build

- Add @pytorch in tools/bazel.bzl (#91424)
- Change visibility for //c10:headers (#91422)
- Simplify OpenMP detection in CMake (#91576)
- Use `@pytorch//` in bazel build files which improves embedding usecases (#89660)
- Enable `USE_CUDA `for bazel build (#92640)
- Add missing default initializers to class members (#94049)

## Jit

- Skip builtins while enumerating class methods (#91805)
- Support lovelace for NVRTC (#87611)
- Expanded symbolic shape support (movedim) (#91696)

## Releng

- Update CI test environment; Add symbolic functions (#94564)
- Import `Literal`, `Protocol`, and `Final` from standard library `typing` as of Python 3.8+ (#94490)
- Add cpuinfo to collect_env.py for new issues reporting which helps triaging on CPU (#93899)
- Refactor nvfuser build (#89621)
- Add error checking to flaky test bot platform parser (#86632)
- Make LazyGraphExecutor extensible (#87218)
- Delete BUILD_SPLIT_CUDA option (#87502)
- Use faster cache flush in triton benchmarking (#88557)
- Guard global observer init against Edge profiler (#86347)

# Bug fixes

## Python API

- Fix as_strided_scatter derivative formula(#87646)
- Add bfloat16 support to torch.prod (#87205)
- Disable dimension wrapping for scalar tensors (#89234)
- Fix SIGSEGV on a big-endian machine when reading pickle data (#92810)
- Fix BC-breaking change to reduction arguments `amin`/`amax` (#93091)
- Fix incorrect tensor storage check (#86845)
- Ensure einsum contracts left to right (#87199)
- Add nondeterministic error for `torch.tensor.scatter` (#88244)
- Fix multi-index for `torch.tensor.index_select` over scalar tensor (#94347)
- Add scalar support for `torch.tensor.where` (#92849)
- Improve error message for unsupported argument types (#87601)
- Change as_strided_scatter’s storage offset default to None from 0 (#87481)
- Make `torch.histc` consistent between CPU and CUDA (#87832)
- Add float to list of allowed ops for serialization (#94910)
- Fix numpy1.24 deprecations in unittests ([#93997] (https://github.com/pytorch/pytorch/pull/93997))
- Properly moving segment_reduce to be private as expected (#93166)

## Autograd API

- Fix behavior of hooks registered to Tensors that had previously been modified in-place (#92734)
  - Previously hooks registered to a tensor after it is modified in-place would erroneously receive the gradients of the output w.r.t. to that tensor before it is modified in-place if that tensor had previously had a hook registered to it before it was modified in-place.
  - See [documentation](https://pytorch.org/docs/2.0/notes/autograd.html#behavior-of-tensor-hooks-when-tensor-is-modified-in-place) for more details about backward hooks execution when tensors are modified in-place.
- Update saved variable hooks to no longer trigger on wrapped numbers (#87316)
- Modifying a view created in no-grad mode in-place no longer triggers an internal assert (#88243)
- Improve error message when saved tensor is detached inplace (#88860)
- Prevent module full_backward_hook from erroring in double backward (#88357)
- Fix forward AD custom Function non-differentiable outputs (#90787)
- Don't materialize forward grad for non-differentiable types (#91183)
- Return input as-is if marked dirty even when requires_grad=False (#91214)
- Fix saved tensor hooks to propogate errors back to python as-is (#94456)
- Fix NumPy broadcasting for backward of `linalg.solve` (#91456), `linalg.lstsq` (#91460)
- Fix torch.var backward when input numel == correction (#94546)
- Fix CopySlices logic to ensure wrapped node runs properly. (#89812)

## torch.nn API

- Fix for RNN-like `Module`s to work with `stateless.functional_call()` (#91111), better error messages (#87442),
- Add missing dim checks `EmbeddingBag` (#85433)
- Fix `Upsample` and `EmbeddingBag` module printing (#93850)
- Fix segfaul in `Conv3D` CPU implementation (#94325)
- Fix overflow issue in `Upsample` (#94290)
- Fix `functiona.pixel_{shuffle,unshuffle}` to consistently return views or not (#86608)
- Fix 64bit indexing `Conv3d()` (#87527), `Upsample()` (#87901)
- Fix preserving requires_grad-ness in fusion utils (#89100)
- Fix support for empty inputs/outputs for `Conv{1,2,3}d()` (#86521), `functional.adaptive_{avg, max}_pool()` (#88906)
- Fix buffer overflow in `Upsample()` (#89252), `MaxUnpool3d()` (#94372)
- Fix `functional.grid_sample()` loss of precision for `torch.float16` inputs (#90427)
- Fix `functional.interpolate()` bicubic interpolation to properly preserve memory format (#90470)

## torch.func

- Fix cross to match unbatched behavior (#86926)
- Properly error on complex inputs or outputs in jacrev, jacfwd (#94805)
- Fix batching rule for dropout (#92975)
- Fix vmap and anomaly mode interaction (#92672)
- Fix and update type hints for `make_functional.py` (#91579)
- torch.tril & torch.tril : add out of bound checks (#89384)
- Fix torch.cat batching rule (#86932)
- Fix reduction boxed batching rules (#91109)

## Cuda

- Check SM version before calling flash attention with BFloat16 (#86600)
- Add range check to multi margin loss target (#89008)
- Fix NVML visible device parsing (#92315)
- Take `CUDA_VISIBLE_DEVICES` into account for nvml calls (#94568)
- Fix topk IMA (#93095)
- Fix: half reduction with multiple sub-iterators (#85596)
- Fix segfault when swapping custom allocator (#89613)
- Conditionally set device in autograd engine (#91191)
- Store `autocast_gpu_dtype` in `custom_fwd` and `custom_bwd` for BFloat16 autocast (#88029)
- Do not use at::cuda::getDefaultCUDAStream() (#91180)
- Ensure that our error handling runs with the GIL enabled (#92848)
- Fix C10_CUDA_CHECK for failing to capture last cuda error occasionally (#93192)
- Fixes a memory leak by making autocast cache global instead of thread-local (#86492)
- Take `CUDA_VISIBLE_DEVICES` into account for nvml calls (#94568)
- Explicitly set the workspace for cuBLAS handles (#86645)

## Cpp API

- Fix CUDNN_PATH handling on Windows (#88898)
- Fix typos in warning/error messages(#88961)
- Remove uneeded checks from embedding bag impl (#92982)
- Fix c++ : segfault in modulelist and moduledict (#93074)

## Visualization

- Fix overflow issue in tensorboard image summary (#90423)
- Remove deprecated call to tf.io.gfile.get_filesystem (#89832)

## NestedTensor API

- Enable non-contiguous Nested Tensors for BMM inputs for NT on CUDA (#88108), linear backward (#94317)
- Fix bug in unsqueeze_nested stride calculation (#88688)

## Distributed

- Distributed(c10d)
  - Fix a static initialization order fiasco in c10d (#90149)
  - Fix `send`, `recv` return type (#92152)
  - Fix MPI backend PG initialization (#92847)
  - Fix header-filter for clang-tidy c10 and apply some fixes to c10 and c10d (#91178)
  - Fix `backend_type` for backend/PG plugin (#93129)
  - Fix UCC PG barrier (#86961)
  - Properly finalize unsuccessful UCC collective posts (#89306)
  - Add pre & post processing for UCC CPU collectives (#89030)
  - Re-enabl `isinstance` with `torch.distributed.ReduceOp` (#87303, #88275)
  - Ameliorate custom `__eq__` for `ReduceOp` (#90088)
  - Fix warning if backend registers timer (#91702)
- DistributedDataParallel
  - Fix DDP when the number of output features is zero (#87793)
- FullyShardedDataParallel
  - Fix `use_orig_params=True` for reentrant activation checkpointing by disabling the post-backward hooks (#87413)
  - Re-establish the wrapped module in `_lazy_init` in case module changing after FSDP constructor (#87837)
  - Fix the incorrect norm calculation for `NO_SHARD` by handling sharded and non-sharded parameters differently in `FSDP.clip_grad_norm_` (#88955)
  - Pass through `ActivationWrapper` directly to the inner wrapped module to fix `state_dict` issues (#87950)
  - Remove the clean of FQNs even for `use_orig_params=True` in FSDP (#91767, #92662)
  - Restrict meta model check to non ignored modules in FSDP (#86766)
  - Fix `keep_low_precision_grads=True` for `use_orig_params=True` (#90027)
  - Fix for `use_orig_params=True` + `no_sync` (#90546)
  - Fix `no_sync`, `use_orig_params=True`, mixed precision, sharded (#92874)
  - Fix input grad propagation when using param mixed precision (#90921)
  - Fix `_mp_shard` in `record_stream` (#91096)
  - Fix "use-after-free" in reshard logic (#94859)
  - Fix `clip_grad_norm_` issues (#94835), (#86337)
  - Fix `load_sharded_state_dict` FQN mismatches for shared parameters (#86524)
  - Fix grad zero vs. `None` edge case (#87308)
  - Fix FSDP `state_dict` transformations of modules with persistent buffers failure with mixed precision enabled (#93396)
  - [FSDP] Fix `nn.Parameter` usage for 2D and `use_orig_params=True` (#89782, #89845, #90562)
- RPC
  - FFixixed use after free in tensorpipe agent (#87627)
- Torch Elastic
  - Make TorchElastic timer importable on Windows (#88522)
- Tensor parallel & 2D parallel
  - Fix the logic to trigger load hooks for 2D parallel integration with FSDP. (#86272)

## Profiler

- Minor bug fixes for ROCM tracing (#89785, #88207)

## Foreach API

- Fix `_foreach_norm` on some tensor sizes (#91844)
- Exempt `_foreach_norm` from autograd_not_implemented_fallback check (#93995)

## Complex API

- Fix serialization of `conj` and `neg_view` (#88182)

## Linalg API

- Add empty tensor check to \_compute_linear_combination (#94245)

## Optimizer API

- Fix discrepancy between mt vs st impl (#92699)
- Do NOT inplace modify gradients (#92706)
- Fix memory leak in \_LRScheduler.step() (#85602)
- Look up `group["capturable"]`, not `defaults["capturable"]` in Adam(W) (#94149)
- `FusedAdam(W)` should take `OptState` into account before unscaling grads (#94060)
- Fix LinearLR scheduler start_factor (#86695)
- Keep AveragedModel buffers in sync when use_buffers=False (#84054)
- Fix OneCycleLR error log (#92040)
- Fix SparseAdam consuming iterator (#86210)
- Fix empty grad support for SparseAdam (#86459)

## Serialization

- Fix set pickle_module if not specified (#88570)
- Explicitly check filelike arg of `torch.save` (#88867)
- Fix dtype mismatch for unallocated storage deserialization (#91285)
- Add float to list of allowed ops (#94910)

## Composability

- Fix segfault in has_torch_function (#88559)
- Fix for usages of **torch_dispatch** with operators that take in an OptionalTensorList argument (#88887)
- Allow direct Tensor constructor to return preexisting PyObject (#92754)
- Add fallthrough kernel for AutogradMeta key (#94603)
- Several fixes to existing primtorch and reference decompositions:
  - `cat`: fix striding (#89332)
  - `prelu`: Fix prelu ref when a.ndim &lt; 2 (#89809)
  - `huber_loss_backward` fix (#86955)
  - `uniform` fix (#90094)
  - `unfold_copy` fix (#86371)
- Fix aliasing for primtorch view meta kernels (#86285)
- Properly compute device for elementwise operations with CPU scalar tensor (#93073)
- Several fixes to existing operators’ meta tensor kernels:
  - aten.\_embedding_bag (#92549)
  - aten.fill\_ (#87493)
  - `aten.group_norm` type promotion fix (#86607)
  - aten.\_cudnn_rnn (#91333)
  - aten.bernoulli (#88676)
  - unsqueeze\_ (#88675)
- Several bug fixes as part of hardening functionalization, which is used in AOTAutograd:
  - fix detach() in functionalization (#87750)
  - fix `torch.as_strided_scatter_backward` memory initialization (#88342)
  - fix functionalization resize stride compute (#94018)
  - fix x.is_contiguous(channels_last) in functionalization (#94195)
  - fix set\_() with functionalization (#90722)
  - check for undefined tensors in advanced indexing during functionalization (#90791)
  - fix some composite compliance ops for functionalization (#86470)
  - Make `aten.copy` preserve strides (#89464)

## Sparse API

- Fixes to `torch.mm`: (#90763), (#90917), (#91094)
- Fix CSR to CSC conversion when given indices of int32 dtype (#91061)
- Fix `mul` when given CUDA CSR Tensor and scalar (#91239)
- Fix conversion from CSC, BSC to COO to only result in coalesced Tensors when appropriate (#91440)
- Fix numel after resizing a CSR/BSR/CSC/BSC tensor. (#91831)
- Fix `torch.triangular_solve` for CSR on CPU when `unitriangular=True`. (#93352)

## Distributions

- Fix philox randn to follow standard normal distribution (#91945)

## Cpu

- Fix access to uninitialized memory in VSX vector functions (#89833)
- Fix buffer overflow from AddressSanitizer checks due to inaccurate bfloat16 representation of large integer (#89210)
- Make torch.histc ignore NaNs on CPU (consistent with CUDA) (#85870)
- Fix vectorized trigonometric functions for VSX (#86453)
- Call `symint::sizes()` instead of `sizes()` on convolution error messages. (#89549)
- Make `torch.linspace` result on CPU consistent with numpy (#89048)
- Remove variable_excluded_from_dispatch() assertion from mkldnncommon (#92168)
- `exponential_` few fixes (1) lambda > 0 (2) mkl kernel to continuous (3) better error log on dtype (#92891)
- Vectorize more stable complex division (#93277)
- `cauchy_` few fixes (1) check gamma > 0 (2) better dtype error log (#93314)

## Intel

- Fix CPU autocast for torch.cat due to the new type ITensorListRef (#87756)
- Add parameters check for torch.\_mkldnn_transpose (#85318)
- Fix build with Intel compiler due to c10/util/TypeIndex.h (#89610)

## Package

- Treat builtins as default extern module (#88385)
- Support pickle version 4 by adding missing ops (#90223)
- Check spec for module source before falling back to file in package exporter (#90258)

## Quantization

- Fix the call to get_executorch_backend_config (#86338)
- Fix weight_dtype and bias_dtype backend_config checks (#86719)
- Respect non_leaf_module_list for activation modules (#88498)
- Fix incorrect integer cast on histogram observer bounds (#90355)
- Improve numerical stability of HistogramObserver (#86522)
- Quant_min typo bugfix in utils.py (#88024)
- Fix fuse_func method overwrite (#87791)
- Fix get_default_qat_qconfig for PT 1.13 (#88876)
- Check the value of numel to avoid segfault (#81547)
- Fix mkldnn quantization issue for weight reorder error (#86876)
- Fix Memory Leak in QNNPACK QSoftmax Op (#89544)
- Copy MHA's batch_first attribute in prepare() (#91680)
- Fix for swap_custom_module_to_observer doing duplicate swaps on the same node.target (#91905)

## Fx

- Correctly restore pybind11 error_already_set (#93238)
- Remove proxy tensor's check for data dependent output (#93265)
- Make ShapeEnv deepcopy-able (#93403)
- Fix SubgraphMatcher for case of no anchor found (#86421)
- Fix for partitioner with symbolic shapes (#86425)
- Fix getitem in partitioner and make metadata storage more consistent (#87012)
- Fix magic method try reverse protocol (#88030)
- Fix FakeTensorProp on Module with Parameters or Buffers (#88700)
- Fix PassManager to not use a class variable mutable list (#89108)
- Prevent tracing when we track_tensor_tree (#89139)
- Make all `make_fx` invocations isolated (opaque to higher `make_fx` invocations) by default (#93290)
- Fix matching args in PatternMatcher (#94375)
- Allow FakeTensorProp to run on graphs traced with some None inputs (#94569)
- Copy codegen in legalize_graph (#90023)
- Fix proxy unwrapping for cond() (#91907)

## ONNX

- Fix `triu`/`tril` operator export with diagonal input (#86843)
- Skip tensor printing during model tracing (#86223)
- Fix `aten::index_put(self, mask, v)` export when `rank(mask) &lt; rank(self)` (#92862)
- Fix 0d-tensor broadcast export (#87211)
- Fix device type detection based on strings (#86168)
- Fix `scatter_add` with different static shape of src and index (#89787)
- Fix `_pad_circular` export (#86984)
- Fix concat with empty tensors (#87620)
- Disable ONNX `ceil_mode` and `count_include_pad` to align torch `ceil_mode` results in corner case (#87892)
- Fix ignored small eps in layer normalization in fp16 (#89869)
- Fix `unconvertible_ops` as per #89261 (#89299)
- Fix `Gather` replacement in `RNN peephole` (#93120)
- Fix `cat` operator for tensors with unknown rank (#94870)
- Fix scalar type analysis for copied constant (#86716)
- Fix scalar type detection for optional tensors (#94427)
- Fix 'prim::PackPadded' shape inference (#91829)
- Add `onnx::Max` into standard Op for scalar type alignment (#88750)
- Add `setType` from user into `InferredType` and `Reliable` in `ConstantValueMap` (#88622)
- Integrate ONNX ATen Fallback export with the new operator registry (#87735)
- Fix ONNX ATen Fallback integration for `BUILD_CAFFE2=0` builds (#88504)
- Fix `torch.autograd.Function.symbolic` method support (#94746)
- Fix `FindCommonAncestor` in `function_extraction` (#86650)
- Update training state logic to support `ScriptedModule` (#86745)

## ROCm

- Fix hipify mapping for cuDeviceGet (#90726)

## Mps

- Fix issues with non-contiguous Tensor handling (#86956, #86958)
- Fix issues with ops implementation `torch.median` (#90326, #88807), `torch.{std,var}` `correction` argument (#91203), `torch.index_select` (#94117, #91064), `torch.cumsum` (#94119), `torch.where` (#86240), `torch.nn.Embedding` (#82809), `torch.nn.Softplus` (#88555), `torch.nn.functional.pad` (#89864), `torch.max` (#91520), padding functions (#91522), `torch.nn.functional.upsample` (#91669), pooling functions (#91519, #94348), `torch.nn.{NLLLoss,SmoothL1Loss}` (#94226), `torch.nn.SoftPlus` (#94256), `torch.masked_fill` (#94263), `torch.fill_` (#94479), `torch.median` (#94489), `torch.nonzero` (#94442), `torch.nn.BatchNorm` (#94351), `torch.{min,max}` (#94386), `torch.nn.GELU` (#94529), `torch.nn.LSTM` (#94889), #95137),`torch.nn.Conv2d`(#95078),`torch.nn.functional.bilinear`(#94892),`torch.copy\_` (#95272),`torch.max_pool2d`(#94963),`torch.div` (#95769)
- Fix issues with `torch.bool` for Unary ops (#91120), scatter ops (#94464),
- Fix issues with `torch.float16` for `torch.nan_to_num` (#94220), `torch.nn.HuberLoss` (#94567)
- Properly raise error for `torch.int64` inputs for `torch.dot` (#94270), `torch.floor_divide` (#94488), `torch.square` (#94766),
- Properly cast `torch.int64` to `torch.int32` for reduction ops and raise warning. (#94484)
- Properly raise unimplemented error for `torch.nn.Conv3d` (#94492),
- Fix data type issues with index_add for non-`torch.float` inputs by casting them to `torch.float` (#88542)
- Fix the high watermark value for unified memory allocation on x86 (#91268)
- Fix handling of ops taking multiple dtypes as input (#91197, #91514)
- Fix handling of channels last for `torch.cat` (#91786, #94662), `torch.Conv2d` (#91822, #94384), `torch.nn.{ELU,ReLU,Hardswish}` (#94664), `torch.nn.BatchNorm` (#94760), `torch.nn.MaxPool2d` (#94877)
- Fix view operations handling (#94259, #94278,#95145, #95762, #95905)
- Fix numerical stability issues with various ops (#94889)
- Fix TORCH_WARN_ONCE (#95559) (#95559)

## Build

- Move incorrectly placed closing curly brace of `extern "C"` block (#87853)
- Set INTERFACE_LINK_DIRECTORIES on caffe2::mkl (#89359)
- Also include MKL_THREAD_LIB in link libraries for caffe2::mkl (#89378)
- Fix MSVC compiler error in basic_ops.h (#93322)
- Fix a bug that redefines \_\_STDC_FORMAT_MACROS (#89310)
- Fix ReplaceWithMaybeCopy test in OSS (#88099)

## Jit

- Fix out-of-bounds error in torch.jit.script for functions with many decorators (#87804)
- Assorted fixes for NNC cpu fuser (#85056, #86788, #88798, #89978)
- Set the correct size of aten tensor in presence of MKL-DNN padding (#86767)
- Fix Scalar(bool) handling in toIValue (#87179)

## Vulkan

- Fix an issue with Vulkan not being able to be compiled on Windows (#92207)
- Fix a possible empty vector dereference in the Vulkan optimization pass (#92918)

## Cudnn

- Fix cudnn RNN reproducibility issue (#90522)
- Fix `benchmark_limit` ignoring failed kernels in FIND (#91032)

## Releng

- Set nvfuser default to disabled, keep CI (#86369)
- Add manual cuda deps search logic (#90411)
- Workaround for NumPy builds that ship with a broken Dlpack deleter (#89759)
- Workaround MSVC ICE due to constexpr char\* template argument (#86288)
- Add define to fix issue with compatibility with latest Windows SDK (#85408)
- Remove invalid git option when updating submodules (#91132)

# Performance

## Python API

- Improve torch.lerp performance on cpu (#84845)
- Improve torch.istft performance (#88060)
- Call view within einsum to remediate MPS regression (#87135)
- Remove unnecessary calls to python builtins(#94323)
- Improve type hints for Module forward hooks (#92061)

## Autograd API

- Use in-place input accumulation fast path for dense Tensors. (#90217)

## torch.nn API

- Improve `functional.interpolate()` speed for `torch.channels_last` (#86361, #86361, #90302)
- Improve performance for `functional.multi_head_attention_forward()` (#93234, #89847)
- Improve performance for `TransformerEncoderLayer()` and `MultiheadAttention()` (#87377, #88488, #88831, #88854, #88970, #91171)
- Improve `SyncBatchNorm()` performance by using the right gathering ops (#89521)
- Improve `ConvTransposed2D()` CPU performance for `torch.{float32, bfloat16}` (#92530)
- Improve `functional.local_response_norm()` performance for 3d inputs (#91052)

## torch.func

- Add vmap batching rule for: `bitwise operators` (#91971), `nansum` & `nanmean` (#91372), `all` & `any` (#91966), `torch.linalg.vander` (#91749), `slogdet` (#86815), `torch.index_fill` (#91364), `narrow_copy` (#88130), `view_copy` (#88150), `greater_equal.Scaler` (#91324)

## Cuda

- Layer norm backward speed gain with warp shuffles (#87445, #87814)
- Avoid unnecessary type casts (#86086)
- Use `atomicAdd` for `bfloat16` in Ampere and above (#84981)

## Cpp API

- Vectorize torch.exp2 on CPU and add complex support (#92115)
- Add various performance fixes to c++ STL usage (#94034)

## NestedTensor API

- Improve performance for NestedTensor `torch.bmm`(#86856), (#85894)
- Remove unnecessary check in `select_nested` (#89150)

## Distributed

- Do not call `pad` in no-padding case(#88769)

## Complex API

- Improve complex `lerp` performance (#84844)

## Mobile

- Passing serialized XNNPACK model by reference (#89089)
- Fix to add multiple outputs for the CoreML delegate (#88345)

## Sparse API

- Improve performance of `mul` when given COO (#86269)
- Improve `to(dtype)` support for all sparse compressed formats (#89055)
- Improve conversion of BSR/BSC to COO using `to_sparse` (#91389)
- Improve `sparse_mask` (#91964)
- Improve `to_dense` backward by removing redundant call to `coalesce` (#92001)
- Improve validation of CSR/CSC/BSR/BSC tensors for low dimensional inputs (#94048)
- Improve torch.sparse.sampled_addmm performance on CPU for CSR inputs (#90978)

## Optimizer API

- Improve foreach implementations by pre-grouping tensors to maximize fast path for `{Adadelta, Adagrad, Adam, Adamax, AdamW, ASGD, NAdam, RAdam, RMSProp, RProp, SGD}`(#92048, #92362, #92363, #92349, #92364, #92365, #92369, #92372, #92338)

## Cpu

- Optimizations for flip (#89414, #91806,#88989, #90013)
- Add fmsub to vectorization primitives (#86568)
- Optimize GELU BFloat16 Impl in CPU path (#79378)
- Fix `biasadd` OMP perf issue for the packed MKL SGEMM (#92300)
- Optimize LogSoftmax by improving thread-allocation in `_vec_log_softmax_lastdim` (#85398)
- BF16 autocast conv transpose 1d/2d/3d for CPU (#92527)
- Add mkl implementation for exponential on CPU (#69967)

## Fx

- Use deque instead of list for BFS (#91139)
- Refactor the dfs cyclic search from recursive to iterative approach (#91042)

## Mps

- Increase performance of `torch.add{cmul,cdiv,mm}`(#94214, #94534)`torch.multinomial` (#86342), faster op launch time (#86437), `torch.linear` (#91114), view handling (#91743, #94218), `convolutions`(#94661), `scatter/gather` (#94663)

## Jit

- Add BFloat16 dtype support for oneDNN Graph JIT fuser (#85591)

## Cudnn

- Improve hot path heuristics performance in V8 (#90811)

# Documentation

## Python API

- Fix various spelling and grammatical errors (#87357, #87583, #88033, #91641, #91871, #86642, #86721, #90110, #87724, #88483, #92049, #92762, #88962)
- Fix the documentation of various functions (#88059, #94545, #86593, #93145, #90071, #87870, #91627, #89910, #79086)
- Fix dev-discuss link in the maintainer docs (#89493)
- Add General Project Policies (#87385)

## Autograd API

- Improve autograd documentation (#89401, #93065)

## torch.nn API

- Improve documentation for: `MaxPool2d` (#86559), `utils.clip_grad_norm_()` (#91312), `Module()` (#87142), `{Unfold,Fold}()` (#88819), `torch.nn.functional.gelu` (#89061), `functional.conv2d` `padding` (#85004), `functional.leaky_relu()` (#94090), `MaxUnpool{1,2,3}D` (#94629)

## NestedTensor API

- Update Persons of Interest (#90069)
- Fix path to nested_tensor in example (#86891)

## Mps

- Add 'mps' to the tensor attributes doc page (#86585)

## Distributed

- Activation checkpointing
  - Clean up comments in activation checkpoint (#86622)
- Distributed (c10d)
  - Improve documentation for various functions (#87018, #94543, #91116,#89905, #86438 )
- DistributedDataParallel
  - Improve Documentation (#86221, #91832)
- RPC
  - Fix non-existing parameters in docstrings in benchmarks (#91115)
- Tensor parallelism and DTensor:
  - Add more clarifications and fix errors in tensor parallelism docs (#94786)
  - Update 2D parallelism API naming and docs (#94771)
- FullyShardedDataParallel
  - Add docs to explain the running the forward pass of of submodules in FSDP (#86343)
  - Clarify warnings to mention collectives (#87478)
  - Remove HSDP Zero-2 from doc (#90503)
  - Improve the comments for FSDP (#92359)
- Distributed Checkpoint
  - Enable documentation for Distributed Checkpoint. (#92813)
- Torch Elastic
  - Fix a minor typo in documentation (#90667)
  - Fix `torch.distributed.run` init connect timeout by comparing `host` with the current IP list (#90221)

## torch.func

- Downgrade the warning about forward-mode AD coverage (#87383)
- Add version selector back to functorch docs (#86602)
- Add documentation for torch.func (#91319)
- Fix AOTAutograd tutorial (#87415)
- Add migration guide from functorch (#91811)
- Improve inplace/view note on copy slices (#89856)
- Add more details to the functorch install page (#86823)

## Linalg API

- Add a note on the stability of linalg functions. (#88313)
- Improve documentation for various linalg functions (#89013,#89383, #91129)

## Composability

- Fix ScalarTensor **repr** in Extending PyTorch example (#86330)
- Fix incorrect wrapping of function decorator (#94446)
- Add **all** to torch.{autograd, fx, cuda} submodules (#85343)

## Dataloader API

- Update dataloader docstring mentioning prefetch factor behavior (#89874)

## Sparse API

- Extend documentation for `to_sparse` (#89912)
- Small correction to `torch.sparse` overview documentation(#93258)

## Optimizer API

- Improve documentation for various optimizers (#91195, #91196, #91881, #89575, #86629, #92111)
- Add general documentation on our algorithm defaults (#95391)

## Serialization

- Fix various spelling and grammatical errors (#90662, #91253)

## Distributions

- Improve documentation for various distributions (#91091, #87577)
- Add original sources/references to Wishart.py in distributions (#86543)

## Quantization

- Improvements to various READMEs (#89319, #86914,#86523, #89795, #90403)
- Add docstrings for operators defined in torch.ops.quantized_decomposed namespace (#89547)
- Add x86 backend as default backend of server inference (#86794)
- Fix non-existing parameters in docstrings in torch/ao (#90875)
- Move parts of BackendConfig tutorial (#91999)

## ONNX

- Fix non-existing parameters in docstrings in torch/onnx (#90593)
- Update diagnostics system (#94565)

## Releng

- Enabled xdoctest runner in CI (#83816)
