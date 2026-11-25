# 企业共建续约预测与定向沟通

季度为自然季度。企业身份、联系许可与决策权限按当时生效资料解释。提案状态只表示合作流程的当前记录。

## 资料

CSV 样例为合成记录，使用 UTF-8，首行为字段名。多值用竖线分隔，空单元格表示来源未填。记录日期和业务生效日期各有含义。

- organizations.csv 的字段为 unit、group、control、sector、from_q、to_q、revision。
- milestones.csv 的字段为 event、unit、quarter、kind、state、observed_on。
- permissions.csv 的字段为 unit、scope、start、stop、expected_hours、version。
- projects.csv 的字段为 program、resource、active_from、active_to、exclusive、contact_hours。
- proposals.csv 的字段为 proposal、unit、program、quarter、status、contacted_on。

## 运行资料检查

在项目根目录使用 Python 3.11 或更高版本。依赖仅为标准库。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
