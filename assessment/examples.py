from general.models import Language

python_start_example = """
    <pre class="prettyprint lang-py">
def f(a):
    # Modify this code to return 'a'
    # multiplied by itself
    return None
    </pre>
"""

python_test_example = """
    <pre class="prettyprint lang-python">
assert f(2) == 4 # assert will output errors to stderr
assert f(0) == 0 # edge case 1
assert f(-1) == 1 # edge case 2
    </pre>
"""

python_solution_example = """
    <pre class="prettyprint lang-python">
def f(a):
    return a*a
    </pre>
"""

java_start_example = """
    <pre class="prettyprint lang-java">
class A {
    public static int f(int a) {
        /* Modify this code to return 'a'
            multiplied by itself */
    	return null;
    }
}
    </pre>
"""

java_test_example = """
    <pre class="prettyprint lang-java">
class Main {
    public static void main(String[] args) {
        if (A.f(2) != 4) {
            System.err.println("f(2) should return 4");
        }
        else if (A.f(0) != 0) {
            System.err.println("f(0) should return 0");
        }
        else if (A.f(-1) != 1) {
            System.err.println("f(-1) should return 1");
        }
    }
}
    </pre>
"""

java_solution_example = """
    <pre class="prettyprint lang-java">
class A {
    public static int f(int a) {
        /* Modify this code to return 'a'
            multiplied by itself */
    	return a*a;
    }
}
    </pre>
"""

ruby_start_example = """
    <pre class="prettyprint lang-ruby">
def f(a)
    # Modify this code to return 'a' multiplied by itself
    return nil
end
    </pre>
"""

ruby_test_example = """
    <pre class="prettyprint lang-ruby">
if f(2) != 4 then
    STDERR.print "f(2) should be 4"
elsif f(0) != 0 then
    STDERR.print "f(0) should be 0"
elsif f(-1) != 1 then
    STDERR.print "f(-1) should be 1"
end
    </pre>
"""

ruby_solution_example = """
    <pre class="prettyprint lang-ruby">
def f(a)
    # Modify this code to return 'a' multiplied by itself
    return a*a
end
    </pre>
"""

javascript_start_example = """
    <pre class="prettyprint lang-js">
function f(a){
    // Modify this code to return 'a' multiplied by itself
    return null;
}
    </pre>
"""

javascript_test_example = """
    <pre class="prettyprint lang-js">
if (f(2) != 4)
    console.error("f(2) is not 4");
else if (f(0) != 0)
    console.error("f(0) is not 0");
else if (f(-1) != 1)
    console.error("f(-1) is not 1");
    </pre>
"""

javascript_solution_example = """
    <pre class="prettyprint lang-js">
function f(a){
    // Modify this code to return 'a' multiplied by itself
    return a*a;
}
    </pre>
"""



def get_start_example(language):
    if language == Language.PYTHON.value:
        return python_start_example
    elif language == Language.JAVA.value:
        return java_start_example
    elif language == Language.RUBY.value:
        return ruby_start_example
    elif language == Language.JAVASCRIPT.value:
        return javascript_start_example
    return python_start_example


def get_test_example(language):
    if language == Language.PYTHON.value:
        return python_test_example
    elif language == Language.JAVA.value:
        return java_test_example
    elif language == Language.RUBY.value:
        return ruby_test_example
    elif language == Language.JAVASCRIPT.value:
        return javascript_test_example
    return python_test_example

def get_solution_example(language):
    if language == Language.PYTHON.value:
        return python_solution_example
    elif language == Language.JAVA.value:
        return java_solution_example
    elif language == Language.RUBY.value:
        return ruby_solution_example
    elif language == Language.JAVASCRIPT.value:
        return javascript_solution_example
    return python_solution_example