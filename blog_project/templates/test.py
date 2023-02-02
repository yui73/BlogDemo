if reg_form.is_valid():
# 注册
    user = User.objects.create(username=reg_form.cleaned_data["username"],
                                email=reg_form.cleaned_data["email"],
                                # url=reg_form.cleaned_data["url"],
                                password=make_password(reg_form.cleaned_data["password"]),)
    user.save()

    # 登录
    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
    login(request, user)
    return redirect(request.POST.get('source_url'))
else:
    # 将报错信息渲染到失败页
    return render(request, 'failure.html', {'reason': reg_form.errors})