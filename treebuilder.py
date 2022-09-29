import re
from branch import Branch, AttributeList
from tags import (HTML5TAGS, SINGLE_HTML5TAGS, SCRIPT_TAGS, SLASH, LT, GT, SPACE)


class Tree:

    def __init__(self):
        self._branches = []

    def get_tree(self):
        return self._branches

    def find(self, tag: str, attrs: dict = None, multiple: bool = False) -> Branch|list:
        if attrs:
            return self._find_by_attrs(tag=tag, attrs=attrs, multiple=multiple)
        else:
            return self._find_by_tag(tag=tag, multiple=multiple)

    def _find_by_tag(self, tag, multiple) -> Branch|list:
        if multiple:
            return [x for x in self._branches if x.tag == tag]
        return [x for x in self._branches if x.tag == tag][0]

    def _find_by_attrs(self, tag, attrs, multiple) -> Branch|list:
        r = [x for x in self._branches if x.tag == tag and self._has_attrs(x, attrs)]
        if r:
            if multiple:
                return r
            return r[0]
        return None

    def _has_attrs(self, branch, attrs):
        r = True
        for k, v in attrs.items():
            if k == "class":
                if not hasattr(branch.attributes, f"{k}_") or v not in getattr(branch.attributes, f"{k}_"):
                    r = False
            elif not hasattr(branch.attributes, k) or getattr(branch.attributes, k) != v:
                r = False
        return r

    def grow_branch(self, branch: Branch):
        self._branches.append(branch)

    def show_tree(self):
        for branch in self._branches:
            print("{} ({}) {} - {} ({})".format("..."*branch.level, branch.id, branch.tag, branch.attributes, branch.content))

    def clear_tree(self):
        self._branches = []


class TreeBuilder:

    def __init__(self):
        self.tree = Tree()
        self._init_variables()

    def _init_variables(self):
        self._inside_script = False

    def build_tree(self, markup: str) -> Tree:
        if markup:
            branches = self._dispatch(markup)
            return self._grow_tree(markup, branches)

    def _grow_tree(self, markup, branches):
        for c, branch in enumerate(branches):
            self.tree.grow_branch(Branch(
                id_=branch["id"],
                level=branch["level"],
                tag=branch["tag"],
                position=branch["position"],
                parent_id=self._get_parent_id(branches[:c], branch["level"]),
                child_set=self._get_child_set(branches[c+1:], branch["level"]),
                attributes=self._get_attr_set(markup, branch["tag"], branch["position"]),
                content=self._get_content(markup, branches[c:]),
            ))
        return self.tree

    def _dispatch(self, markup):
        id_, level, position = 0, 0, 0
        branches = []
        while position < markup.__len__():
            p = markup.find(LT, position)
            if p == -1:
                break
            tag = self._extract_tag_name(markup[p+1:])
            if tag:
                if self._is_open_html5tag(tag):
                    branches.append({
                        "id": id_,
                        "tag": tag,
                        "position": p,
                        "level": level,
                    })
                    id_ += 1
                    if not self._is_single_html5tag(tag):
                        level += 1
                if self._is_close_html5tag(tag):
                    level -= 1
            position = p + 1

        return branches if branches else None

    # # парсер не только HTML5 элементов
    # def _is_open_html5tag(self, tag):
    #     if tag[0] != SLASH:
    #         if self._is_script(tag):
    #             self._inside_script = True
    #         if not self._inside_script or self._is_script(tag):
    #             return True
    #     return False
    #
    # def _is_close_html5tag(self, tag):
    #     if tag[0] == SLASH:
    #         if self._is_script(tag.strip(SLASH)):
    #             self._inside_script = False
    #         if not self._inside_script:
    #             return True
    #     return False
    # #

    def _is_open_html5tag(self, tag):
        if self._is_script(tag):
            self._inside_script = True
        if (tag in HTML5TAGS and not self._inside_script) or self._is_script(tag):
            return True
        return False

    def _is_close_html5tag(self, tag):
        if tag[0] == SLASH:
            if self._is_script(tag.strip(SLASH)):
                self._inside_script = False
            if tag.strip(SLASH) in HTML5TAGS and not self._inside_script:
                return True
        return False

    def _is_single_html5tag(self, tag):
        return True if tag in SINGLE_HTML5TAGS else False

    def _is_script(self, tag):
        return True if tag in SCRIPT_TAGS else False

    def _extract_tag_name(self, markup):
        tag = ''
        p = 0
        while markup[p].isalpha() or markup[p] == SLASH or markup[p] == "-":
            tag += markup[p]
            p += 1
        return tag

    def _get_parent_id(self, branches, level):
        for branch in reversed(branches):
            if branch["level"] < level:
                return branch["id"]
        return None

    def _get_child_set(self, branches, level):
        child_set = []
        for branch in branches:
            if branch["level"] == level:
                break
            if branch["level"] == level + 1:
                child_set.append(branch["id"])
        return None if not child_set else child_set

    def _get_attr_set(self, markup, tag, position):
        attributes_dict = {}
        inside_value = False
        inside_key = True
        key, value = '', ''
        p = position + tag.__len__() + 1
        while markup[p] != GT or inside_value:
            c = markup[p]
            if inside_key:
                if c == " ":
                    if key:
                        key = key.replace("-", "_")
                        attributes_dict[key] = True
                    key = ''
                elif c == "=":
                    inside_key = False
                else:
                    key += c
            elif inside_value:
                if c == "\"":
                    if key == "class":
                        attributes_dict["class_"] = value.split(" ")
                    else:
                        key = key.replace("-", "_")
                        attributes_dict[key] = value
                    inside_value = False
                    key = ''
                    value = ''
                else:
                    value += c
                p += 1
                continue
            elif c == " " and not inside_value and not inside_key:
                inside_key = True
            elif c == "\"" and not inside_value and not inside_key:
                inside_value = True
            p += 1
        return attributes_dict

    def _get_content(self, markup, slice_branches):
        for branch in slice_branches:
            if branch["level"] == slice_branches[0]["level"] or branch["level"] > slice_branches[0]["level"]:
                return self._crop_content(markup[branch["position"]:slice_branches[0]["position"]])
        return self._crop_content(markup[branch["position"]:])

    def _crop_content(self, content):
        s = ''
        in_tag = False
        for c in content:
            if c == LT:
                in_tag = True
                continue
            if c == GT:
                in_tag = False
                continue
            if not in_tag:
                s += c
        return s if s else None
